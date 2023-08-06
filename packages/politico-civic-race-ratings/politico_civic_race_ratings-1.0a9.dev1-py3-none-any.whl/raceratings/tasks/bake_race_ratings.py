# Imports from python.
import json
import logging


# Imports from other dependencies.
from celery import chord
from celery import shared_task
from geography.models import DivisionLevel
from government.models import Jurisdiction
import us


# Imports from race_ratings.
from raceratings.models import ExportRecord
from raceratings.tasks.utils.queries.ratings import filter_races
from raceratings.tasks.utils.workflow import gather_all_files
from raceratings.tasks.utils.io.ratings import create_race_rating_json
from raceratings.tasks.utils.io.ratings import create_race_rating_json_for_body
from raceratings.tasks.utils.io.ratings import upload_file
from raceratings.utils.sitemap import generate_sitemap


FED_GOVT_ID = (
    Jurisdiction.objects.filter(name="U.S. Federal Government")
    .values_list("id", flat=True)
    .get()
)

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def bake_sitemap(task_config):
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    sitemap_races = generate_sitemap(election_year)

    s3_file_location = upload_file("sitemap.json", json.dumps(sitemap_races))

    return [s3_file_location]


@shared_task(acks_late=True)
def bake_electoral_college_ratings(task_config):
    """Bake electoral-college list and detail JSON files.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        electoral-college.json
        /electoral-college
            /me.json
            /me-02.json
    """
    election_year = task_config.get("election_year")
    include_special_elections = task_config.get("include_special_elections")

    races = filter_races(
        (election_year, include_special_elections), dict()
    ).order_by("division__label")

    electoral_college_races = races.filter_by_body("electoral-college")

    race_list_file = create_race_rating_json_for_body(
        "electoral-college.json", electoral_college_races, "electoral-college"
    )

    files_created = [race_list_file]

    for race in electoral_college_races:
        if race.division.level.slug == DivisionLevel.STATE:
            state_abbrev = us.states.lookup(race.division.code).abbr.lower()

            destination_filename = f"{state_abbrev}.json"
        else:
            state_abbrev = us.states.lookup(
                race.division.parent.code
            ).abbr.lower()

            destination_filename = f"{state_abbrev}-{race.division.code}.json"

        per_race_file = create_race_rating_json(
            f"electoral-college/{destination_filename}", race
        )

        files_created.append(per_race_file)

    return files_created


@shared_task(acks_late=True)
def bake_senate_ratings(task_config):
    """Bake senate list and detail JSON files.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        senate.json
        /senate
            /ga.json
            /ga-special.json
    """
    election_year = task_config.get("election_year")
    include_special_elections = task_config.get("include_special_elections")

    races = filter_races(
        (election_year, include_special_elections), dict()
    ).order_by("office__division__label")

    senate_races = races.filter_by_body("senate")

    race_list_file = create_race_rating_json_for_body(
        "senate.json", senate_races, "senate"
    )

    files_created = [race_list_file]

    for race in senate_races:
        state_abbrev = us.states.lookup(race.office.division.code).abbr.lower()

        destination_filename = (
            f"{state_abbrev}-special.json"
            if race.special
            else f"{state_abbrev}.json"
        )

        per_race_file = create_race_rating_json(
            f"senate/{destination_filename}", race
        )

        files_created.append(per_race_file)

    return files_created


@shared_task(acks_late=True)
def bake_house_ratings(task_config):
    """Bake house list and detail JSON files.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        house.json
        /house
            /ia-03.json
            /tx-32.json
    """
    election_year = task_config.get("election_year")
    include_special_elections = task_config.get("include_special_elections")

    races = filter_races(
        (election_year, include_special_elections), dict()
    ).order_by("office__division__label")

    house_races = races.filter_by_body("house")

    race_list_file = create_race_rating_json_for_body(
        "house.json", house_races, "house"
    )

    files_created = [race_list_file]

    for race in house_races:
        state_abbrev = us.states.lookup(
            race.office.division.parent.code
        ).abbr.lower()

        destination_filename = (
            f"{state_abbrev}-{race.office.division.code}-special.json"
            if race.special
            else f"{state_abbrev}-{race.office.division.code}.json"
        )

        per_race_file = create_race_rating_json(
            f"house/{destination_filename}", race
        )

        files_created.append(per_race_file)

    return files_created


@shared_task(acks_late=True)
def bake_governor_ratings(task_config):
    """Bake senate list and detail JSON files.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        governors.json
        /governors
            /de.json
    """
    election_year = task_config.get("election_year")
    include_special_elections = task_config.get("include_special_elections")

    races = filter_races(
        (election_year, include_special_elections), dict()
    ).order_by("office__division__label")

    governor_races = races.filter_by_body("governorships")

    race_list_file = create_race_rating_json_for_body(
        "governors.json", governor_races, "governors"
    )

    files_created = [race_list_file]

    for race in governor_races:
        state_abbrev = us.states.lookup(race.office.division.code).abbr.lower()

        destination_filename = f"{state_abbrev}.json"

        per_race_file = create_race_rating_json(
            f"governors/{destination_filename}", race
        )

        files_created.append(per_race_file)

    return files_created


@shared_task(acks_late=True)
def bake_per_state_ratings(task_config):
    """Bake electoral-college list and detail JSON files.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /by-state
            /me.json
            /me-02.json
    """
    election_year = task_config.get("election_year")
    include_special_elections = task_config.get("include_special_elections")

    races = filter_races(
        (election_year, include_special_elections), dict()
    ).order_by(
        "office__short_label",
        "office__body__organization__founding_date",
        "-office__body__slug",
        "office__division__code",
    )

    files_created = []

    for state in us.states.STATES:
        races_for_state = races.filter_by_state(state.abbr)

        destination_filename = f"{state.abbr.lower()}.json"

        per_state_file = create_race_rating_json(
            f"by-state/{destination_filename}", races_for_state
        )

        files_created.append(per_state_file)

    return files_created


@shared_task(acks_late=True, bind=True)
def bake_all_race_ratings(self, task_config):
    bodies_to_bake = task_config.get("bodies")

    summaries_pluralized = "reports" if len(bodies_to_bake) > 1 else "report"

    joined_bodies = ", ".join(
        [*bodies_to_bake[:-2], *[" and ".join(bodies_to_bake[-2:])]]
    )

    logger.info(f"Baking {summaries_pluralized} for {joined_bodies}...")

    export_record_props = dict(
        task_id=self.request.id,
        record_type=ExportRecord.RACE_RATINGS_TYPE,
        status=ExportRecord.IN_PROGRESS_STATUS,
    )

    ExportRecord.objects.create(**export_record_props)

    baking_tasks = [
        bake_sitemap.si(task_config),
        bake_per_state_ratings.si(task_config),
    ]

    if "house" in bodies_to_bake:
        baking_tasks.append(bake_house_ratings.si(task_config))

    if "senate" in bodies_to_bake:
        baking_tasks.append(bake_senate_ratings.si(task_config))

    if "president" in bodies_to_bake:
        baking_tasks.append(bake_electoral_college_ratings.si(task_config))

    if "governors" in bodies_to_bake:
        baking_tasks.append(bake_governor_ratings.si(task_config))

    publish_queue = chord(
        baking_tasks, gather_all_files.s(export_record_props),
    )

    publish_queue.apply_async()
