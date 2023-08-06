# Imports from Django.
from django.core.exceptions import ObjectDoesNotExist


# Imports from other dependencies.
from civic_utils.serializers import CommandLineListSerializer
from civic_utils.serializers import NaturalKeySerializerMixin
from election.models import Race
from election.models import Election
from election.models import ElectionType
from elections import ElectionYear
from geography.models import DivisionLevel
from government.models import Jurisdiction
from rest_framework.reverse import reverse
from rest_framework import serializers


# Imports from race_ratings.
from raceratings.models import RatingPageContent
from raceratings.serializers.candidate import CandidateSerializer
from raceratings.serializers.category import CategorySerializer
from raceratings.serializers.race_rating import RaceRatingAdminSerializer
from raceratings.serializers.race_rating import RaceRatingSerializer


FED_GOVT_ID = (
    Jurisdiction.objects.filter(name="U.S. Federal Government")
    .values_list("id", flat=True)
    .get()
)


class RaceListSerializer(NaturalKeySerializerMixin, CommandLineListSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            "raceratings_api_race-detail",
            request=self.context["request"],
            kwargs={"pk": obj.pk},
        )

    class Meta(CommandLineListSerializer.Meta):
        model = Race
        fields = ("url", "uid", "label")


class RaceAPISerializer(CommandLineListSerializer):
    rating_category = serializers.SerializerMethodField()
    candidates = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    primary_dates = serializers.SerializerMethodField()
    is_special = serializers.SerializerMethodField()
    senate_class = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.ELECTION_YEAR = ElectionYear(2020)
        super(RaceAPISerializer, self).__init__(*args, **kwargs)

    def get_rating_category(self, obj):
        return obj.rating_category

    def get_candidates(self, obj):
        try:
            gnl_election_for_race = obj.elections.all()[0]

            return CandidateSerializer(
                [
                    _.candidate
                    for _ in gnl_election_for_race.candidate_elections.all()
                ],
                many=True,
            ).data
        except IndexError:
            return []

    def get_label(self, obj):
        if not obj.office.body:
            if obj.division:
                label = "{} [{} electoral vote(s)]".format(
                    obj.office.label, obj.division.label
                )
            else:
                label = obj.office.label
        else:
            if obj.office.body.slug == "senate":
                label = "{} Senate".format(obj.office.division.label)
            elif obj.office.body.slug == "house":
                label = "{}, District {}".format(
                    obj.office.division.parent.label,
                    obj.office.division.code
                    if not obj.office.division.code.endswith("00")
                    else "At-Large",
                )

        if obj.special:
            label = "{}, Special Election".format(label)

        return label

    def get_id(self, obj):
        # for easier search
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            postal = obj.office.division.parent.code_components["postal"]
            code = obj.office.division.code
            return "{}-{}".format(postal, code)

        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.slug == DivisionLevel.STATE:
                postal = obj.division.code_components["postal"]
                return "{}-{}".format(postal, "potus")

            postal = obj.division.parent.code_components["postal"]
            return "{}_{}-{}".format(postal, obj.division.code, "potus")

        postal = obj.office.division.code_components["postal"]

        if obj.office.body:
            base = "{}-{}".format(postal, "sen")

            return "{}-{}".format(base, "special") if obj.special else base

        return "{}-{}".format(postal, "gov")

    def get_body(self, obj):
        if obj.office.body:
            return obj.office.body.slug

        return (
            "president"
            if obj.office.division.level.slug == DivisionLevel.COUNTRY
            else "governor"
        )

    def get_state(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return obj.office.division.parent.code
        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.name == DivisionLevel.DISTRICT:
                return obj.division.parent.code
            return obj.division.code
        else:
            return obj.office.division.code

    def get_primary_dates(self, obj):
        party_primary_dates = {}

        if obj.office.division.level.slug == DivisionLevel.COUNTRY:
            state_fips = obj.division.code_components["fips"]["state"]

            presidential_for_state = self.ELECTION_YEAR.elections_for_state(
                state_fips
            ).presidential_primaries

            if any(
                [
                    len(presidential_for_state.democratic) > 0,
                    len(presidential_for_state.republican) > 0,
                ]
            ):
                if len(presidential_for_state.democratic) > 0:
                    party_primary_dates[
                        "dem"
                    ] = presidential_for_state.democratic[
                        0
                    ].election_date.strftime(
                        "%Y-%m-%d"
                    )

                if len(presidential_for_state.republican) > 0:
                    party_primary_dates[
                        "gop"
                    ] = presidential_for_state.republican[
                        0
                    ].election_date.strftime(
                        "%Y-%m-%d"
                    )

            return party_primary_dates

        elif obj.office.division.level.slug == DivisionLevel.STATE:
            state_fips = obj.office.division.code_components["fips"]["state"]
        elif obj.office.division.level.slug == DivisionLevel.DISTRICT:
            state_fips = obj.office.division.code_components["fips"]["state"]

        if not state_fips:
            return party_primary_dates

        downticket_for_state = self.ELECTION_YEAR.elections_for_state(
            state_fips
        ).downticket_primaries

        if len(downticket_for_state) == 0:
            return party_primary_dates

        if any(
            [
                len(downticket_for_state.democratic) > 0,
                len(downticket_for_state.republican) > 0,
            ]
        ):
            if len(downticket_for_state.democratic) > 0:
                party_primary_dates["dem"] = downticket_for_state.democratic[
                    0
                ].election_date.strftime("%Y-%m-%d")

            if len(downticket_for_state.republican) > 0:
                party_primary_dates["gop"] = downticket_for_state.republican[
                    0
                ].election_date.strftime("%Y-%m-%d")
        elif all(
            [
                len(downticket_for_state) == 1,
                downticket_for_state[0].election_variant
                in [
                    ElectionType.MAJORITY_ELECTS_BLANKET_PRIMARY,
                    ElectionType.TOP_TWO_PRIMARY,
                ],
            ]
        ):
            party_primary_dates["dem"] = downticket_for_state[
                0
            ].election_date.strftime("%Y-%m-%d")
            party_primary_dates["gop"] = downticket_for_state[
                0
            ].election_date.strftime("%Y-%m-%d")

        return party_primary_dates

    def get_is_special(self, obj):
        return obj.special

    def get_senate_class(self, obj):
        if obj.office.body:
            if all(
                [
                    obj.office.body.jurisdiction_id == FED_GOVT_ID,
                    obj.office.body.slug == "senate",
                ]
            ):
                return int(obj.office.senate_class)
        return None

    def get_district(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return "{}-{}".format(
                obj.office.division.parent.code, obj.office.division.code
            )
        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.name == DivisionLevel.DISTRICT:
                return "{}-{}".format(
                    obj.division.parent.code, obj.division.code
                )

        return None

    class Meta(CommandLineListSerializer.Meta):
        model = Race
        fields = (
            "rating_category",
            "candidates",
            "label",
            "id",
            "pk",
            "body",
            "state",
            "primary_dates",
            "is_special",
            "electoral_votes",
            "senate_class",
            "district",
            "description",
        )

    def to_representation(self, obj):
        serialized_repr = super(RaceAPISerializer, self).to_representation(obj)

        if serialized_repr["primary_dates"] is None:
            serialized_repr.pop("primary_dates")

        if serialized_repr["electoral_votes"] is None:
            serialized_repr.pop("electoral_votes")

        if serialized_repr["senate_class"] is None:
            serialized_repr.pop("senate_class")

        if serialized_repr["district"] is None:
            serialized_repr.pop("district")

        return serialized_repr


class RaceSerializer(NaturalKeySerializerMixin, CommandLineListSerializer):
    ratings = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()

    def get_ratings(self, obj):
        return RaceRatingSerializer(obj.ratings, many=True).data

    def get_content(self, obj):
        return RatingPageContent.objects.race_content(obj)

    def get_office(self, obj):
        if not obj.office.body:
            label = obj.office.label
        else:
            if obj.office.body.slug == "senate":
                label = "{} Senate".format(obj.office.division.label)
            elif obj.office.body.slug == "house":
                label = "{}, District {}".format(
                    obj.office.division.parent.label, obj.office.division.code
                )

        if obj.special:
            label = "{}, Special Election".format(label)

        return label

    class Meta(CommandLineListSerializer.Meta):
        model = Race
        fields = ("uid", "ratings", "content", "office")


class RaceAdminSerializer(CommandLineListSerializer):
    ratings = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()

    # a bunch of search fields
    abbrev = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_ratings(self, obj):
        return RaceRatingAdminSerializer(obj.ratings.all(), many=True).data

    def get_office(self, obj):
        if obj.office.body and obj.office.body.slug == "senate":
            label = "{} {}".format(obj.office.division.label, "Senate")
        elif not obj.office.body and obj.office.jurisdiction_id == FED_GOVT_ID:
            verbose_geography = (
                obj.division.label
                if obj.division.level.slug == DivisionLevel.STATE
                else " ".join(
                    [
                        obj.division.parent.label,
                        "District",
                        f"{int(obj.division.code)}",
                    ]
                )
            )
            votes_pluralized = (
                "votes"
                if obj.division.level.slug == DivisionLevel.STATE
                else "vote"
            )

            label = f"{verbose_geography} electoral college {votes_pluralized}"
        else:
            label = obj.office.label

        if obj.special:
            return "{} Special".format(label)
        else:
            return label

    def get_abbrev(self, obj):
        # for easier search
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            postal = obj.office.division.parent.code_components["postal"]
            code = int(obj.office.division.code)
            return "{}-{}".format(postal, code)
        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.slug == DivisionLevel.STATE:
                postal = obj.division.code_components["postal"]
                return "{}-{}".format(postal, "potus")
            else:
                postal = obj.division.parent.code_components["postal"]
                return "{}_{}-{}".format(postal, obj.division.code, "potus")
        else:
            postal = obj.office.division.code_components["postal"]

            if obj.office.body:
                return "{}-{}".format(postal, "sen")
            else:
                return "{}-{}".format(postal, "gov")

    def get_code(self, obj):
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            return int(obj.office.division.code)
        else:
            return 0

    class Meta(CommandLineListSerializer.Meta):
        model = Race
        fields = ("uid", "ratings", "office", "abbrev", "code", "special")
