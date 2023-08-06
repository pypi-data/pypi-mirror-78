# Imports from Django.
# from django.core.exceptions import MultipleObjectsReturned


# Imports from other dependencies.
from election.models import CandidateElection
from election.models import ElectionType


# Imports from race_ratings.
from raceratings.tasks.utils.candidate_overrides import CANDIDATE_OVERRIDES
from raceratings.tasks.utils.candidate_overrides import RUNOFF_DATES
from raceratings.tasks.utils.candidate_overrides import SECOND_RUNOFF_OVERRIDES
from raceratings.tasks.utils.candidate_overrides import WINNER_OVERRIDES


def find_candidate(raceid, polnum, include_party=False, is_runoff=False):
    formatted_polnum = f"polnum-{polnum}"

    matching_election_types = [
        ElectionType.PRIMARY_RUNOFF
    ] if is_runoff else [
        ElectionType.PARTISAN_PRIMARY,
        ElectionType.PARTISAN_CAUCUS,
        ElectionType.TOP_TWO_PRIMARY,
        ElectionType.MAJORITY_ELECTS_BLANKET_PRIMARY,
    ]

    try:
        candidate_object = CandidateElection.objects.get(
            ap_candidate_number=formatted_polnum,
            election__ap_election_id=raceid,
            election__election_ballot__election_event__election_type__slug__in=[
                *matching_election_types
            ],
        )

        candidate_meta = dict(
            firstName=candidate_object.candidate.person.first_name,
            middleName=candidate_object.candidate.person.middle_name,
            lastName=candidate_object.candidate.person.last_name,
            suffix=candidate_object.candidate.person.suffix,
            incumbent=candidate_object.candidate.incumbent,
        )

        if include_party:
            candidate_meta[
                "party"
            ] = candidate_object.candidate.party.ap_code.lower()

        return candidate_meta
    except CandidateElection.DoesNotExist:
        if (
            raceid in CANDIDATE_OVERRIDES
            and polnum in CANDIDATE_OVERRIDES[raceid]
        ):
            return CANDIDATE_OVERRIDES[raceid][polnum]
        else:
            print(
                " ".join(
                    [
                        "Could not find candidate with #",
                        f'"{raceid}__{formatted_polnum}".',
                    ]
                )
            )

            candidate_meta = dict(
                firstName="",
                middleName="",
                lastName="",
                suffix="",
                incumbent="",
            )

            if include_party:
                candidate_meta["party"] = ""

            return candidate_meta
    # except MultipleObjectsReturned:
    #     print(f"{raceid}")


def process_runoff_participant(raceid, raw_polnum, vote_order):
    candidate_metadata = find_candidate(raceid, raw_polnum)

    return dict(**candidate_metadata, voteOrder=vote_order)


def get_top_two_winner_config(result_data):
    top_two_primary_winners = dict(placeOne=None, placeTwo=None)

    found_winners = [_ for _ in result_data if _["winner"] == "True"]

    # topTwoPrimaryUnopposed
    # topTwoPrimaryOutright
    # topTwoPrimaryTBD
    # "placeOne": {"type": "topTwoPrimaryOutright", "firstName": "Zoe", "lastName": "Lofgren", "party": "dem", "incumbent": true},
    # "placeTwo": {"type": "topTwoPrimaryTBD"}

    if len(result_data) > 0:
        race_id = result_data[0]["raceid"]

        if race_id in SECOND_RUNOFF_OVERRIDES:
            found_winners = [
                dict(raceid=race_id, polnum=polnum)
                for polnum in SECOND_RUNOFF_OVERRIDES[race_id]
            ]

    if len(found_winners) > 0:
        candidate_one_metadata = find_candidate(
            found_winners[0]["raceid"],
            found_winners[0]["polnum"],
            include_party=True,
        )

        top_two_primary_winners["placeOne"] = dict(
            type="topTwoPrimaryOutright", **candidate_one_metadata
        )

        if len(found_winners) > 1:
            candidate_two_metadata = find_candidate(
                found_winners[1]["raceid"],
                found_winners[1]["polnum"],
                include_party=True,
            )

            top_two_primary_winners["placeTwo"] = dict(
                type="topTwoPrimaryOutright", **candidate_two_metadata
            )
        else:
            raceid = found_winners[0]["raceid"]
            print(f'No second top-two winner found in race #"{raceid}"')

            top_two_primary_winners["placeTwo"] = dict(type="topTwoPrimaryTBD")
    else:
        top_two_primary_winners["placeOne"] = dict(type="topTwoPrimaryTBD")
        top_two_primary_winners["placeTwo"] = dict(type="topTwoPrimaryTBD")

    if len(found_winners) == len(result_data) and len(found_winners) > 1:
        top_two_primary_winners["placeOne"]["type"] = "topTwoPrimaryUnopposed"

        if len(found_winners) == 2:
            top_two_primary_winners["placeTwo"][
                "type"
            ] = "topTwoPrimaryUnopposed"

    return top_two_primary_winners


def get_partisan_winner_config(result_data, party_slug, is_runoff=False):
    results_for_party = [
        _
        for _ in result_data
        if _["party"].lower() == party_slug
        and _["race_type_slug"] != "general"
    ]

    race_ids_for_party = list(
        set([result_row["raceid"] for result_row in results_for_party])
    )

    race_id = "///"
    if len(race_ids_for_party) == 1:
        race_id = race_ids_for_party[0]

    found_winner = [_ for _ in results_for_party if _["winner"] == "True"]

    if len(found_winner) > 0:
        candidate_metadata = find_candidate(
            found_winner[0]["raceid"],
            found_winner[0]["polnum"],
            include_party=False,
            is_runoff=is_runoff
        )

        found_runners_up = [
            _
            for _ in results_for_party
            if _["polnum"] != found_winner[0]["polnum"]
        ]

        if len(found_runners_up) > 0:
            win_type = "runoffWinner" if is_runoff else "outright"

            return dict(
                type=win_type,
                **candidate_metadata,
                margin=round(
                    (
                        float(found_winner[0]["votepct"])
                        - float(found_runners_up[0]["votepct"])
                    )
                    * 100,
                    2,
                ),
            )
        else:
            return dict(type="unopposed", **candidate_metadata)
    elif race_id in WINNER_OVERRIDES:
        overridden_winner = [
            _
            for _ in results_for_party
            if _["polnum"] == WINNER_OVERRIDES[race_id]
        ]

        candidate_metadata = find_candidate(
            race_id,
            overridden_winner[0]["polnum"],
            include_party=False,
            is_runoff=is_runoff
        )

        found_runners_up = [
            _
            for _ in results_for_party
            if _["polnum"] != overridden_winner[0]["polnum"]
        ]

        if len(found_runners_up) > 0:
            win_type = "runoffWinner" if is_runoff else "outright"

            return dict(
                type=win_type,
                **candidate_metadata,
                margin=round(
                    (
                        float(overridden_winner[0]["votepct"])
                        - float(found_runners_up[0]["votepct"])
                    )
                    * 100,
                    2,
                ),
            )
        else:
            return dict(type="unopposed", **candidate_metadata)

    found_runoffs = [_ for _ in results_for_party if _["runoff"] == "True"]

    if len(results_for_party) > 0:
        race_id = results_for_party[0]["raceid"]

        if race_id in SECOND_RUNOFF_OVERRIDES:
            found_runoffs = [
                dict(raceid=race_id, polnum=polnum)
                for polnum in SECOND_RUNOFF_OVERRIDES[race_id]
            ]

    if len(found_runoffs) > 0:
        runoff_participants = []

        runoff_participants.append(
            process_runoff_participant(
                found_runoffs[0]["raceid"],
                found_runoffs[0]["polnum"],
                vote_order=1,
            )
        )

        if len(found_runoffs) > 1:
            runoff_participants.append(
                process_runoff_participant(
                    found_runoffs[0]["raceid"],
                    found_runoffs[1]["polnum"],
                    vote_order=2,
                )
            )
        else:
            raceid = found_runoffs[0]["raceid"]
            print(f'No second runoff winner found in race #"{raceid}"')
            runoff_participants.append(dict(type="in-progress"))

        return dict(
            type="runoff",
            runoffDate=RUNOFF_DATES[results_for_party[0]["statepostal"]],
            runoffParticipants=runoff_participants,
        )

    return None
