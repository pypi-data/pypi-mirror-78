# Imports from python.
import logging


# Imports from Django.
from django.utils import timezone


# Imports from other dependencies.
from celery import shared_task


# Imports from race_ratings.
from raceratings.models import ExportRecord


logger = logging.getLogger("tasks")


@shared_task(bind=True)
def gather_all_files(self, grouped_files, export_record_props=None):
    created_files = [
        file
        for per_task_file_list in grouped_files
        for file in per_task_file_list
        if isinstance(per_task_file_list, list)
    ]

    created_files.extend(
        [file for file in grouped_files if not isinstance(file, list)]
    )

    logger.info(f"Created {len(created_files)} file(s).")

    if export_record_props:
        record = ExportRecord.objects.get(**export_record_props)
        record.end_time = timezone.now()
        record.status = ExportRecord.SUCCESS_STATUS
        record.save()

        logger.info(f"  > Finished in {record.duration} seconds.")

    return created_files
