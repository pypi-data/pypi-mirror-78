# Imports from Django.
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery


# Imports from other dependencies.
from election.models import CandidateElection
from election.models import Election
from election.models import ElectionType
from election.models import Race


# Imports from race_ratings.
from raceratings.models import DataProfile
from raceratings.models import RaceRating


def filter_races(required_args, extra_constraints={}):
    election_year, include_special_elections = required_args

    race_query = {"cycle__slug": election_year, **extra_constraints}

    if not include_special_elections:
        race_query["special"] = False

    races = (
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
        .annotate(
            rating_category=Subquery(
                RaceRating.objects.select_related("category")
                .filter(race_id=OuterRef("pk"))
                .order_by("-created")
                .values("category__short_label")[:1]
            ),
            rating_created=Subquery(
                RaceRating.objects.select_related("category")
                .filter(race_id=OuterRef("pk"))
                .order_by("-created")
                .values("created")[:1]
            ),
            # primary_dates=Subquery(
            #     DataProfile.objects.filter(race_id=OuterRef("pk"))
            #     .order_by("-created")
            #     .values("data")[:1]
            # ),
        )
        .exclude(office__body__slug="house", special=True)
        .filter(**race_query)
    )

    return races
