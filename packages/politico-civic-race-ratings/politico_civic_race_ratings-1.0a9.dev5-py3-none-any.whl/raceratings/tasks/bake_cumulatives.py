# Imports from python.
import json
import logging


# Imports from other dependencies.
from celery import chord
from celery import shared_task
from elections import ElectionYear
import us


# Imports from race_ratings.
from raceratings.models import ExportRecord
from raceratings.tasks.bootstrap_cumulatives import (
    bootstrap_cumulative_rollups,
)
from raceratings.tasks.utils.candidate_overrides import PRIMARY_DATE_OVERRIDES
from raceratings.tasks.utils.io.cumulatives import upload_file
from raceratings.tasks.utils.queries.cumulatives import get_races_for_body
from raceratings.tasks.utils.workflow import gather_all_files


logger = logging.getLogger("tasks")


def get_date_for_state_contest(election_year_raw, state_abbr, election_mode):
    election_year = ElectionYear(election_year_raw)

    if state_abbr in PRIMARY_DATE_OVERRIDES[election_mode]:
        return PRIMARY_DATE_OVERRIDES[election_mode][state_abbr]

    elections_for_state = election_year.elections_for_state(state_abbr)

    if election_mode == "downticket":
        matching_primary = elections_for_state.downticket_primaries[0]
    elif election_mode == "president":
        matching_primary = elections_for_state.presidential_primaries[0]
    else:
        return None

    return matching_primary.election_date.strftime("%Y-%m-%d")


def get_incumbent_party_for_seat(election_year_raw, state_slug, **kwargs):
    election_year = ElectionYear(election_year_raw)

    if "district_number" in kwargs:
        formatted_district_number = (
            str(int(kwargs["district_number"]))
            if kwargs["district_number"] != "00"
            else None
        )

        seat = next(
            (
                seat
                for seat in election_year.federal.congress.seats.house
                if seat.state.fips == us.states.lookup(state_slug).fips
                and seat.district == formatted_district_number
            )
        )
    elif "senate_class" in kwargs:
        seat = next(
            (
                seat
                for seat in election_year.federal.congress.seats.senate
                if seat.state.fips == us.states.lookup(state_slug).fips
                and seat.senate_class == kwargs["senate_class"]
            )
        )
    else:
        formatted_state_slug = (
            us.states.lookup(state_slug).name.lower().replace(" ", "_")
        )

        seat = getattr(
            election_year.states, formatted_state_slug
        ).executive.chief

    if seat.incumbent_party is None:
        return None

    return seat.incumbent_party.ap_code.lower()


@shared_task(acks_late=True)
def bake_house_winner_summaries(task_config):
    election_year_raw = task_config.get("electionYear")

    winner_listings = bootstrap_cumulative_rollups(election_year_raw, "house")

    all_races = get_races_for_body(election_year_raw, "house")

    def get_seat_key(race, district_number_override=None):
        if district_number_override is not None:
            raw_district_number = district_number_override
        else:
            raw_district_number = race.office.division.code

        state_name = race.office.division.parent.name
        district_number = raw_district_number.zfill(2)

        return f"{us.states.lookup(state_name).abbr}-{district_number}"

    formatted_races = []

    for race in all_races:
        observed_winners = winner_listings.get(get_seat_key(race), None)

        if observed_winners is None and race.office.division.code == "00":
            observed_winners = winner_listings.get(
                get_seat_key(race, "1"), None
            )

        formatted_races.append(
            dict(
                state=race.office.division.parent.name,
                district=race.office.division.code.zfill(2),
                primaryDate=get_date_for_state_contest(
                    election_year_raw,
                    us.states.lookup(race.office.division.parent.name).abbr,
                    "downticket",
                ),
                incumbentParty=get_incumbent_party_for_seat(
                    election_year_raw=election_year_raw,
                    state_slug=race.office.division.parent.name,
                    district_number=race.office.division.code,
                ),
                winners=observed_winners,
                electionForecastRating=race.rating_category.lower(),
            )
        )

    all_winners = [
        {
            k: v
            for k, v in formatted_race.items()
            if v is not None or k == "incumbentParty"
        }
        for formatted_race in formatted_races
    ]

    all_winners_json = json.dumps(all_winners)

    upload_path = "summary/house.json"

    s3_file_location = upload_file(upload_path, all_winners_json)

    return s3_file_location


@shared_task(acks_late=True)
def bake_senate_winner_summaries(task_config):
    election_year_raw = task_config.get("electionYear")

    winner_listings = bootstrap_cumulative_rollups(election_year_raw, "senate")

    all_races = get_races_for_body(election_year_raw, "senate")

    def get_seat_key(race):
        if race.special:
            return "-".join(
                [
                    f"{us.states.lookup(race.office.division.name).abbr}-SEN",
                    "SPECIAL",
                ]
            )

        return f"{us.states.lookup(race.office.division.name).abbr}-SEN"

    def get_primary_date(race):
        state_abbr = us.states.lookup(race.office.division.name).abbr
        if race.special and state_abbr == "GA":
            return "2020-11-03"

        return get_date_for_state_contest(
            election_year_raw, state_abbr, "downticket"
        )

    formatted_races = [
        dict(
            state=race.office.division.name,
            primaryDate=get_primary_date(race),
            incumbentParty=get_incumbent_party_for_seat(
                election_year_raw=election_year_raw,
                state_slug=race.office.division.name,
                senate_class="".rjust(int(race.office.senate_class), "I"),
            ),
            winners=winner_listings.get(get_seat_key(race), None),
            electionForecastRating=race.rating_category.lower(),
            isSpecial=race.special,
        )
        for race in all_races
        if race.rating_category is not None
    ]

    all_winners = [
        {k: v for k, v in formatted_race.items() if v is not None}
        for formatted_race in formatted_races
    ]

    all_winners_json = json.dumps(all_winners)

    upload_path = "summary/senate.json"

    s3_file_location = upload_file(upload_path, all_winners_json)

    return s3_file_location


@shared_task(acks_late=True)
def bake_president_winner_summaries(task_config):
    election_year_raw = task_config.get("electionYear")

    winner_listings = bootstrap_cumulative_rollups(
        election_year_raw, "president"
    )

    all_races = get_races_for_body(election_year_raw, "president")

    formatted_races = [
        dict(
            state=race.division.name,
            primaryDate=get_date_for_state_contest(
                election_year_raw,
                us.states.lookup(race.division.name).abbr,
                "president",
            ),
            winners=winner_listings.get(
                f"{us.states.lookup(race.division.name).abbr}-POTUS", None
            ),
            electionForecastRating=race.rating_category.lower(),
        )
        for race in all_races
    ]

    all_winners = [
        {k: v for k, v in formatted_race.items() if v is not None}
        for formatted_race in formatted_races
    ]

    all_winners_json = json.dumps(all_winners)

    upload_path = "summary/president.json"

    s3_file_location = upload_file(upload_path, all_winners_json)

    return s3_file_location


@shared_task(acks_late=True)
def bake_governor_winner_summaries(task_config):
    election_year_raw = task_config.get("electionYear")

    winner_listings = bootstrap_cumulative_rollups(
        election_year_raw, "governor"
    )

    all_races = get_races_for_body(election_year_raw, "governors")

    formatted_races = [
        dict(
            state=race.office.division.name,
            primaryDate=get_date_for_state_contest(
                election_year_raw,
                us.states.lookup(race.office.division.name).abbr,
                "downticket",
            ),
            incumbentParty=get_incumbent_party_for_seat(
                election_year_raw=election_year_raw,
                state_slug=race.office.division.name,
            ),
            winners=winner_listings.get(
                f"{us.states.lookup(race.office.division.name).abbr}-GOV", None
            ),
            electionForecastRating=race.rating_category.lower(),
        )
        for race in all_races
    ]

    all_winners = [
        {k: v for k, v in formatted_race.items() if v is not None}
        for formatted_race in formatted_races
    ]

    all_winners_json = json.dumps(all_winners)

    upload_path = "summary/governors.json"

    s3_file_location = upload_file(upload_path, all_winners_json)

    return s3_file_location


@shared_task(acks_late=True, bind=True)
def bake_all_winner_summaries(self, task_config):
    bodies_to_bake = task_config.get("bodies")

    summaries_pluralized = (
        "summary" if len(bodies_to_bake) > 1 else "summaries"
    )

    joined_bodies = ", ".join(
        [*bodies_to_bake[:-2], *[" and ".join(bodies_to_bake[-2:])]]
    )

    logger.info(f"Baking {summaries_pluralized} for {joined_bodies}...")

    export_record_props = dict(
        task_id=self.request.id,
        record_type=ExportRecord.CUMULATIVE_RECORDS_TYPE,
        status=ExportRecord.IN_PROGRESS_STATUS,
    )

    ExportRecord.objects.create(**export_record_props)

    baking_tasks = []

    if "house" in bodies_to_bake:
        baking_tasks.append(bake_house_winner_summaries.si(task_config,))

    if "senate" in bodies_to_bake:
        baking_tasks.append(bake_senate_winner_summaries.si(task_config,))

    if "president" in bodies_to_bake:
        baking_tasks.append(bake_president_winner_summaries.si(task_config,))

    if "governors" in bodies_to_bake:
        baking_tasks.append(bake_governor_winner_summaries.si(task_config,))

    publish_queue = chord(
        baking_tasks, gather_all_files.s(export_record_props,),
    )

    publish_queue.apply_async()
