# Imports from python.
from datetime import datetime
from datetime import time
from itertools import chain, groupby


# Imports from Django.
from django.db.models import DateField
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import Subquery
from django.db.models.functions import Trunc
from django.utils.timezone import make_aware


# Imports from other dependencies.
from django_filters import rest_framework as filters
from election.models import CandidateElection
from election.models import Election
from election.models import ElectionType
from election.models import Race
from geography.models import Division
from geography.models import DivisionLevel
from government.models import Body
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
import us


# Imports from race_ratings.
from raceratings.conf import settings
from raceratings.models import Category
from raceratings.models import DataProfile
from raceratings.models import RaceRating
from raceratings.serializers import BodyRatingSerializer
from raceratings.serializers import CategorySerializer
from raceratings.serializers import DistrictSerializer
from raceratings.serializers import RaceAPISerializer
from raceratings.serializers import RaceRatingDeltaSerializer

# from raceratings.serializers import RaceRatingFeedSerializer
from raceratings.serializers import StateSerializer
from raceratings.utils.api_auth import CsrfExemptSessionAuthentication
from raceratings.utils.api_auth import TokenAPIAuthentication
from raceratings.viewsets.filters import RaceRatingsFilters


class BodyRatingsViewSet(APIView):
    def get(self, request, format=None):
        data = []
        bodies = Body.objects.all()

        for body in bodies:
            latest_rating = body.ratings.latest("created")
            data.append(BodyRatingSerializer(latest_rating).data)

        return Response(data)


class RaceRatingDeltasViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = RaceRating.objects.all()
    serializer_class = RaceRatingDeltaSerializer

    def get_queryset(self):
        cycle_race_ids = Race.objects.filter_by_cycle(
            self.kwargs["year"]
        ).values_list("id")

        rating_start_date = datetime.strptime(
            getattr(settings, "OPEN_DATE", "2019-01-01"), "%Y-%m-%d"
        ).date()

        date_threshold = make_aware(
            datetime.combine(rating_start_date, time.min)
        )

        return (
            RaceRating.objects.select_related(
                "category",
                "race",
                "race__division",
                "race__division__level",
                "race__division__parent",
                "race__office",
                "race__office__body",
                "race__office__division",
                "race__office__division__level",
                "race__office__division__parent",
            )
            .exclude(created__lt=date_threshold)
            .annotate(
                created_day=Trunc("created", "day", output_field=DateField()),
                most_recent_past_category_id=Subquery(
                    RaceRating.objects.filter(race_id=OuterRef("race_id"))
                    .exclude(created__gte=OuterRef("created"))
                    .order_by("-created")
                    .values("category_id")[:1]
                ),
            )
            .filter(race_id__in=cycle_race_ids)
            .order_by(
                "-created_day",
                "race__office__division__parent__code",
                "race__office__division__code",
            )
        )


class RaceRatingsViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Race.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RaceRatingsFilters
    # filter_class = ''
    serializer_class = RaceAPISerializer

    def get_queryset(self):
        return (
            Race.objects.prefetch_related(
                Prefetch(
                    "elections",
                    queryset=Election.objects.prefetch_related(
                        Prefetch(
                            "candidate_elections",
                            queryset=CandidateElection.objects.select_related(
                                "election",
                                "candidate",
                                "candidate__party",
                                "candidate__person",
                            ),
                        )
                    )
                    .select_related(
                        "race",
                        "election_ballot",
                        "election_ballot__election_event",
                        "election_ballot__election_event__election_type",
                    )
                    .filter(
                        **{
                            "__".join(
                                [
                                    "election_ballot",
                                    "election_event",
                                    "election_type",
                                    "slug",
                                ]
                            ): ElectionType.GENERAL
                        }
                    )
                    .order_by(
                        "race_id",
                        "election_ballot__election_event__election_type__slug",
                    ),
                )
            )
            .select_related(
                "cycle",
                "division",
                "division__level",
                "division__parent",
                "office",
                "office__body",
                "office__body__organization",
                "office__division",
                "office__division__level",
                "office__division__parent",
            )
            .filter(cycle__slug=self.kwargs["year"])
            .exclude(office__body__slug="house", special=True)
            .annotate(
                rating_category=Subquery(
                    RaceRating.objects.select_related("category")
                    .filter(race_id=OuterRef("pk"))
                    .order_by("-created")
                    .values("category__short_label")[:1]
                ),
                # primary_dates=Subquery(
                #     DataProfile.objects.filter(race_id=OuterRef("pk"))
                #     .order_by("-created")
                #     .values("data")[:1]
                # ),
            )
            .order_by("office__division__label")
        )

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        lookup_value = self.kwargs[lookup_url_kwarg]

        is_special_election = False
        if lookup_value.endswith("-special"):
            is_special_election = True
            lookup_value = lookup_value.replace("-special", "")

        if lookup_value.endswith("-potus"):
            lookup_value = lookup_value.replace("-potus", "")

            if len(lookup_value) == 2:
                filter_kwargs = dict(
                    office__body__isnull=True,
                    office__division__level__slug=DivisionLevel.COUNTRY,
                    division__level__slug=DivisionLevel.STATE,
                    division__code=us.states.lookup(lookup_value).fips,
                    special=is_special_election,
                )
            else:
                state_abbrev = lookup_value[:2]
                district_abbrev = lookup_value[-2:]
                filter_kwargs = dict(
                    office__body__isnull=True,
                    office__division__level__slug=DivisionLevel.COUNTRY,
                    division__level__slug=DivisionLevel.DISTRICT,
                    division__parent__code=us.states.lookup(state_abbrev).fips,
                    division__code=district_abbrev,
                    special=is_special_election,
                )
        elif lookup_value.endswith("-sen"):
            lookup_value = lookup_value.replace("-sen", "")

            filter_kwargs = dict(
                office__body__slug="senate",
                office__division__level__slug=DivisionLevel.STATE,
                office__division__code=us.states.lookup(lookup_value).fips,
                special=is_special_election,
            )
        elif lookup_value.endswith("-gov"):
            lookup_value = lookup_value.replace("-gov", "")

            filter_kwargs = dict(
                office__body__isnull=True,
                office__division__level__slug=DivisionLevel.STATE,
                office__division__code=us.states.lookup(lookup_value).fips,
                special=is_special_election,
            )
        else:
            filter_kwargs = {}
            state_abbrev = lookup_value[:2]
            district_abbrev = lookup_value[-2:]

            filter_kwargs = dict(
                office__body__slug="house",
                office__division__level__slug=DivisionLevel.DISTRICT,
                office__division__parent__code=us.states.lookup(
                    state_abbrev
                ).fips,
                office__division__code=district_abbrev,
                special=is_special_election,
            )

        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class RaceRatingsAPIViewSet(APIView):
    def get(self, request, format=None):
        races = Race.objects.filter(
            cycle__slug="2020", special=False
        ).order_by("office__division__label")

        race_data = RaceAPISerializer(races, many=True).data

        return Response(race_data)


class RaceRatingsFeedViewSet(APIView):
    def get(self, request, format=None):
        races = Race.objects.filter(
            cycle__slug="2020", special=False
        ).order_by("office__division__label")

        races = races

        ratings = [race.ratings.order_by("created")[1:] for race in races]
        ratings = list(chain(*ratings))
        ratings = sorted(ratings, key=lambda r: r.created)
        grouped = {}
        for key, group in groupby(ratings, lambda r: r.created):
            date = key.strftime("%Y-%m-%d")

            # grouped[date] = [
            #     RaceRatingFeedSerializer(rating).data for rating in list(group)
            # ]

        return Response(grouped)


class RaceRatingsFilterViewSet(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        states = Division.objects.filter(level__name=DivisionLevel.STATE)
        districts = Division.objects.filter(level__name=DivisionLevel.DISTRICT)

        categories_data = CategorySerializer(categories, many=True).data
        states_data = StateSerializer(states, many=True).data
        districts_data = DistrictSerializer(districts, many=True).data

        data = {
            "categories": categories_data,
            "states": states_data,
            "districts": districts_data,
        }

        return Response(data)
