# Imports from python.
import json
import logging


# Imports from other dependencies.
from celery import chord
from celery import shared_task


# Imports from race_ratings.
from raceratings.models import ExportRecord
from raceratings.models import RaceRating
from raceratings.tasks.utils.deltas import generate_delta_page
from raceratings.tasks.utils.deltas import get_changed_ratings
from raceratings.tasks.utils.deltas import split_days_into_pages
from raceratings.tasks.utils.io.ratings import upload_file
from raceratings.tasks.utils.workflow import gather_all_files


logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def bake_overall_deltas(task_config):
    """Bake 'rating changelist' JSON files for all bodies and races.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /changelist
            /page-001.json
            /page-002.json
    """
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    changed_ratings = get_changed_ratings(election_year, None)

    day_pages = split_days_into_pages(changed_ratings)

    files_created = []

    for i, days_on_current_page in enumerate(day_pages):
        current_page = i + 1

        page_filename, page_payload = generate_delta_page(
            None,
            current_page,
            days_on_current_page,
            changed_ratings,
            len(day_pages),
        )

        s3_file_location = upload_file(page_filename, json.dumps(page_payload))

        files_created.append(s3_file_location)

    if not day_pages:
        blank_filename, blank_payload = generate_delta_page(
            None, 1, [], RaceRating.objects.none(), 1
        )

        s3_file_location = upload_file(
            blank_filename, json.dumps(blank_payload)
        )

        files_created.append(s3_file_location)

    return files_created


@shared_task(acks_late=True)
def bake_electoral_college_deltas(task_config):
    """Bake 'rating changelist' JSON files for the electoral college.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /electoral-college
            /changelist
                /page-001.json
                /page-002.json
    """
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    changed_ratings = get_changed_ratings(election_year, "electoral-college")

    day_pages = split_days_into_pages(changed_ratings)

    files_created = []

    for i, days_on_current_page in enumerate(day_pages):
        current_page = i + 1

        page_filename, page_payload = generate_delta_page(
            "electoral-college",
            current_page,
            days_on_current_page,
            changed_ratings,
            len(day_pages),
        )

        s3_file_location = upload_file(page_filename, json.dumps(page_payload))

        files_created.append(s3_file_location)

    if not day_pages:
        blank_filename, blank_payload = generate_delta_page(
            "electoral-college", 1, [], RaceRating.objects.none(), 1
        )

        s3_file_location = upload_file(
            blank_filename, json.dumps(blank_payload)
        )

        files_created.append(s3_file_location)

    return files_created


@shared_task(acks_late=True)
def bake_senate_deltas(task_config):
    """Bake 'rating changelist' JSON files for the U.S. Senate.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /senate
            /changelist
                /page-001.json
                /page-002.json
    """
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    changed_ratings = get_changed_ratings(election_year, "senate")

    day_pages = split_days_into_pages(changed_ratings)

    files_created = []

    for i, days_on_current_page in enumerate(day_pages):
        current_page = i + 1

        page_filename, page_payload = generate_delta_page(
            "senate",
            current_page,
            days_on_current_page,
            changed_ratings,
            len(day_pages),
        )

        s3_file_location = upload_file(page_filename, json.dumps(page_payload))

        files_created.append(s3_file_location)

    if not day_pages:
        blank_filename, blank_payload = generate_delta_page(
            "senate", 1, [], RaceRating.objects.none(), 1
        )

        s3_file_location = upload_file(
            blank_filename, json.dumps(blank_payload)
        )

        files_created.append(s3_file_location)

    return files_created


@shared_task(acks_late=True)
def bake_house_deltas(task_config):
    """Bake 'rating changelist' JSON files for the U.S. House.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /house
            /changelist
                /page-001.json
                /page-002.json
    """
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    changed_ratings = get_changed_ratings(election_year, "house")

    day_pages = split_days_into_pages(changed_ratings)

    files_created = []

    for i, days_on_current_page in enumerate(day_pages):
        current_page = i + 1

        page_filename, page_payload = generate_delta_page(
            "house",
            current_page,
            days_on_current_page,
            changed_ratings,
            len(day_pages),
        )

        s3_file_location = upload_file(page_filename, json.dumps(page_payload))

        files_created.append(s3_file_location)

    if not day_pages:
        blank_filename, blank_payload = generate_delta_page(
            "house", 1, [], RaceRating.objects.none(), 1
        )

        s3_file_location = upload_file(
            blank_filename, json.dumps(blank_payload)
        )

        files_created.append(s3_file_location)

    return files_created


@shared_task(acks_late=True)
def bake_governor_deltas(task_config):
    """Bake 'rating changelist' JSON files for gubernatorial races.

    URLs of data produced (on S3, under UPLOADED_FILES_PREFIX):

        /governors
            /changelist
                /page-001.json
                /page-002.json
    """
    election_year = task_config.get("election_year")
    # include_special_elections = task_config.get("include_special_elections")

    changed_ratings = get_changed_ratings(election_year, "governorships")

    day_pages = split_days_into_pages(changed_ratings)

    files_created = []

    for i, days_on_current_page in enumerate(day_pages):
        current_page = i + 1

        page_filename, page_payload = generate_delta_page(
            "governors",
            current_page,
            days_on_current_page,
            changed_ratings,
            len(day_pages),
        )

        s3_file_location = upload_file(page_filename, json.dumps(page_payload))

        files_created.append(s3_file_location)

    if not day_pages:
        blank_filename, blank_payload = generate_delta_page(
            "governors", 1, [], RaceRating.objects.none(), 1
        )

        s3_file_location = upload_file(
            blank_filename, json.dumps(blank_payload)
        )

        files_created.append(s3_file_location)

    return files_created


@shared_task(acks_late=True, bind=True)
def bake_all_race_rating_deltas(self, task_config):
    bodies_to_bake = task_config.get("bodies")

    summaries_pluralized = (
        "delta reports" if len(bodies_to_bake) > 1 else "delta report"
    )

    joined_bodies = ", ".join(
        [*bodies_to_bake[:-2], *[" and ".join(bodies_to_bake[-2:])]]
    )

    logger.info(f"Baking {summaries_pluralized} for {joined_bodies}...")

    export_record_props = dict(
        task_id=self.request.id,
        record_type=ExportRecord.RATING_DELTAS_TYPE,
        status=ExportRecord.IN_PROGRESS_STATUS,
    )

    ExportRecord.objects.create(**export_record_props)

    baking_tasks = [
        bake_overall_deltas.si(task_config),
    ]

    if "house" in bodies_to_bake:
        baking_tasks.append(bake_house_deltas.si(task_config))

    if "senate" in bodies_to_bake:
        baking_tasks.append(bake_senate_deltas.si(task_config))

    if "president" in bodies_to_bake:
        baking_tasks.append(bake_electoral_college_deltas.si(task_config))

    if "governors" in bodies_to_bake:
        baking_tasks.append(bake_governor_deltas.si(task_config))

    publish_queue = chord(
        baking_tasks, gather_all_files.s(export_record_props),
    )
    publish_queue.apply_async()
