# Imports from python.
from itertools import groupby


# Imports from Django.
# from django.db.models import OuterRef
# from django.db.models import Subquery


# Imports from other dependencies.
from election.models import Election
from election.models import ElectionBallot
from election.models import ElectionDataURL
from election.models import ElectionEvent
from election.models import ElectionType
import us


# Imports from race_ratings.
# from raceratings.tasks.utils.queries.cumulatives import get_races_for_body
from raceratings.tasks.utils.candidate_overrides import UNTRACKED_CONTESTS
from raceratings.tasks.utils.fetch_csv import fetch_csv
from raceratings.tasks.utils.winner_summaries import get_partisan_winner_config
from raceratings.tasks.utils.winner_summaries import get_top_two_winner_config


def create_race_key(raw_race, body):
    state_object = us.states.lookup(raw_race["statepostal"])

    if body == "house":
        return f"{raw_race['statepostal']}-{raw_race['seatnum'].zfill(2)}"
    elif body == "senate":
        try:
            race_obj = Election.objects.get(
                ap_election_id=raw_race["raceid"],
                race__office__division__code=state_object.fips,
                race__office__senate_class__isnull=False,
            ).race

            if race_obj.special:
                return f'{raw_race["statepostal"]}-SEN-SPECIAL'
        except Election.DoesNotExist:
            pass

        return f'{raw_race["statepostal"]}-SEN'
    elif body == "president":
        return f'{raw_race["statepostal"]}-POTUS'
    elif body == "governor":
        return f'{raw_race["statepostal"]}-GOV'

    return raw_race["raceid"]


def bootstrap_cumulative_rollups(election_year, body):
    if body == "president":
        election_types_for_body = [
            ElectionBallot.PRESIDENTIAL_OFFICE,
            ElectionBallot.ALL_OFFICES,
        ]
    else:
        election_types_for_body = [
            ElectionBallot.DOWNTICKET_OFFICES,
            ElectionBallot.ALL_OFFICES,
        ]

    elections_for_body = (
        ElectionEvent.objects.filter(
            election_day__cycle__name=election_year,
            ballots__offices_elected__in=election_types_for_body,
            # election_type__slug__in=ElectionType.PRIMARY_ELECTION_TYPES,
            election_type__slug__in=[
                ElectionType.PARTISAN_PRIMARY,
                ElectionType.PARTISAN_CAUCUS,
                ElectionType.TOP_TWO_PRIMARY,
                ElectionType.MAJORITY_ELECTS_BLANKET_PRIMARY,
            ],
        )
        .select_related("election_type")
        .prefetch_related("ballots", "data_urls")
        .distinct()
    )

    california_primary = (
        ElectionEvent.objects.filter(
            election_day__cycle__name=election_year,
            division__slug__in=["california"],
            election_type__slug__in=[
                ElectionType.PARTISAN_PRIMARY,
                ElectionType.PARTISAN_CAUCUS,
                ElectionType.TOP_TWO_PRIMARY,
                ElectionType.MAJORITY_ELECTS_BLANKET_PRIMARY,
            ],
            data_urls__isnull=False,
        )
        .select_related("election_type")
        .prefetch_related("ballots", "data_urls")
        .distinct()
    )

    california_top_two_event = ElectionEvent.objects.get(
        division__slug="california",
        election_type__slug="top-two-primary",
        election_day__cycle__name=election_year,
    )

    # california_top_two_race_ids = list(
    #     california_top_two_event.ballots.get().elections.values_list(
    #         "ap_election_id", flat=True
    #     )
    # )

    runoffs_for_body = (
        ElectionEvent.objects.filter(
            election_day__cycle__name="2020",
            ballots__offices_elected__in=election_types_for_body,
            election_type__slug=ElectionType.PRIMARY_RUNOFF,
        )
        .select_related("election_type")
        .prefetch_related("ballots", "data_urls")
        .distinct()
    )

    runoff_configs = {}

    for runoff in list(runoffs_for_body):
        if runoff.election_mode != ElectionEvent.UPCOMING_MODE:
            if runoff.data_urls.count() == 0:
                continue

            try:
                state_data_url = (
                    runoff.data_urls.filter(
                        url_type=ElectionDataURL.POLLED_URL_TYPE,
                        url_descriptor="state",
                    )
                    .values_list("url_path", flat=True)
                    .get()
                )
            except ElectionDataURL.DoesNotExist:
                continue

            try:
                state_data = [
                    result_row
                    for result_row in fetch_csv(state_data_url)
                    if result_row["office_slug"] == body
                ]
            except Exception:
                continue

            for race_key, race_data in groupby(
                sorted(
                    state_data,
                    key=lambda i: (i["raceid"], -1 * int(i["votecount"])),
                    # reverse=True,
                ),
                key=lambda i: create_race_key(i, body),
            ):
                all_race_data = list(race_data)

                if race_key not in runoff_configs:
                    runoff_configs[race_key] = {
                        "election_event": runoff,
                        "state_results": [],
                        "callOverrides": [],
                    }

                runoff_configs[race_key]["state_results"].extend(all_race_data)

            raceid_key_map = {
                value["state_results"][0]["raceid"]: key
                for key, value in runoff_configs.items()
                if value["state_results"]
            }

            try:
                call_overrides_url = (
                    runoff.data_urls.filter(
                        url_type=ElectionDataURL.POLLED_URL_TYPE,
                        url_descriptor="callOverrides",
                    )
                    .values_list("url_path", flat=True)
                    .get()
                )
            except ElectionDataURL.DoesNotExist:
                call_overrides_url = None

            if call_overrides_url is not None:
                try:
                    call_overrides = fetch_csv(call_overrides_url)

                    for override in call_overrides:
                        if override["raceid"] in raceid_key_map:
                            race_key = raceid_key_map[override["raceid"]]

                            runoff_configs[race_key]["callOverrides"].append(
                                dict(override)
                            )
                except Exception:
                    pass

    election_configs = {}

    for election in list(elections_for_body) + list(california_primary):
        if election.election_mode != ElectionEvent.UPCOMING_MODE:
            if election.data_urls.count() == 0:
                continue

            try:
                state_data_url = (
                    election.data_urls.filter(
                        url_type=ElectionDataURL.POLLED_URL_TYPE,
                        url_descriptor="state",
                    )
                    .values_list("url_path", flat=True)
                    .get()
                )
            except ElectionDataURL.DoesNotExist:
                continue

            try:
                state_data = [
                    result_row
                    for result_row in fetch_csv(state_data_url)
                    if result_row["office_slug"] == body
                ]
            except Exception:
                continue

            for race_key, race_data in groupby(
                sorted(
                    state_data,
                    key=lambda i: (i["raceid"], -1 * int(i["votecount"])),
                    # reverse=True,
                ),
                key=lambda i: create_race_key(i, body),
            ):
                all_race_data = list(race_data)
                if body != "president" and race_key.startswith("CA"):
                    election = california_top_two_event
                    all_race_data = [
                        row
                        for row in all_race_data
                        if row["race_type_slug"] == "topTwoPrimary"
                    ]

                if race_key not in election_configs:
                    election_configs[race_key] = {
                        "election_event": election,
                        "state_results": [],
                        "callOverrides": [],
                    }

                election_configs[race_key]["state_results"].extend(
                    all_race_data
                )

            raceid_key_map = {
                candidate_row["raceid"]: race_key
                for race_key, race_rows in election_configs.items()
                for candidate_row in race_rows["state_results"]
                if race_rows["state_results"]
            }

            try:
                call_overrides_url = (
                    election.data_urls.filter(
                        url_type=ElectionDataURL.POLLED_URL_TYPE,
                        url_descriptor="callOverrides",
                    )
                    .values_list("url_path", flat=True)
                    .get()
                )
            except ElectionDataURL.DoesNotExist:
                call_overrides_url = None

            if call_overrides_url is not None:
                try:
                    call_overrides = fetch_csv(call_overrides_url)

                    for override in call_overrides:

                        if override["raceid"] in raceid_key_map:
                            race_key = raceid_key_map[override["raceid"]]

                            election_configs[race_key]["callOverrides"].append(
                                dict(override)
                            )
                except Exception:
                    pass

    cumulative_summaries = {}

    for race_id, race_config in election_configs.items():
        if race_id in runoff_configs:
            race_config["runoff_config"] = runoff_configs[race_id]

        race_summary = generate_cumulative_summary(body=body, **race_config)

        if race_summary is not None:
            cumulative_summaries[race_id] = race_summary

        if race_id in UNTRACKED_CONTESTS[body]:
            per_race_overrides = UNTRACKED_CONTESTS[body][race_id]

            for winner_type, winner_config in per_race_overrides.items():
                cumulative_summaries[race_id][winner_type] = winner_config

    return {**UNTRACKED_CONTESTS[body], **cumulative_summaries}


def apply_manual_overrides(race_config):
    base_results = race_config["state_results"]
    in_house_overrides = race_config["callOverrides"]

    overridden_ids = []
    patched_results = []

    for override in in_house_overrides:
        if override["winner"] is True or override["winner"].lower() == "true":
            result_to_override = [
                _
                for _ in base_results
                if _["raceid"] == override["raceid"]
                and _["polnum"] == override["polnum"]
            ]

            if len(result_to_override) == 1:
                row_to_override = result_to_override[0]

                row_to_override["winner"] = "True"
                patched_results.append(row_to_override)

                overridden_ids.append(override["polnum"])

    all_other_results = [
        _ for _ in base_results if _["polnum"] not in overridden_ids
    ]

    patched_results.extend(all_other_results)

    return patched_results


def generate_cumulative_summary(body, election_event, **additional_config):
    winner_summary = {}

    if "runoff_config" in additional_config:
        runoff_summary_data = apply_manual_overrides(
            additional_config["runoff_config"]
        )

    summary_data = apply_manual_overrides(additional_config)

    dem_data = [
        _
        for _ in summary_data
        if _["party"].lower() == "dem" and _["race_type_slug"] != "general"
    ]

    gop_data = [
        _
        for _ in summary_data
        if _["party"].lower() == "gop" and _["race_type_slug"] != "general"
    ]

    null_dem_option = dict(type="in-progress")
    null_gop_option = dict(type="in-progress")

    if all(
        [
            election_event.election_mode == ElectionEvent.PAST_MODE,
            len(dem_data) == 0,
        ]
    ):
        null_dem_option = dict(type="nobody-ran")

    if all(
        [
            election_event.election_mode == ElectionEvent.PAST_MODE,
            len(gop_data) == 0,
        ]
    ):
        null_gop_option = dict(type="nobody-ran")

    if (
        election_event.election_type.slug
        in [ElectionType.PARTISAN_CAUCUS, ElectionType.PARTISAN_PRIMARY]
        and election_event.division.slug == "california"
        and body != "president"
    ):
        return None

    if (
        election_event.election_type.slug
        in [ElectionType.PARTISAN_CAUCUS, ElectionType.PARTISAN_PRIMARY]
        # and election_event.division.slug != "california"
    ):
        dem_summary = get_partisan_winner_config(summary_data, "dem")

        if dem_summary is not None:
            if all(
                [
                    dem_summary.get("type", "") == "runoff",
                    "runoff_config" in additional_config,
                ]
            ):
                runoff_summary = get_partisan_winner_config(
                    runoff_summary_data, "dem", is_runoff=True
                )
                if runoff_summary is not None:
                    dem_summary = runoff_summary

        winner_summary["dem"] = (
            dem_summary if dem_summary is not None else null_dem_option
        )

        gop_summary = get_partisan_winner_config(summary_data, "gop")

        if gop_summary is not None:
            if all(
                [
                    gop_summary.get("type", "") == "runoff",
                    "runoff_config" in additional_config,
                ]
            ):
                runoff_summary = get_partisan_winner_config(
                    runoff_summary_data, "gop", is_runoff=True
                )
                if runoff_summary is not None:
                    gop_summary = runoff_summary

        winner_summary["gop"] = (
            gop_summary if gop_summary is not None else null_gop_option
        )
    elif election_event.election_type.slug in [
        ElectionType.MAJORITY_ELECTS_BLANKET_PRIMARY,
        ElectionType.TOP_TWO_PRIMARY,
    ]:
        winner_summary = get_top_two_winner_config(summary_data)

    return winner_summary
