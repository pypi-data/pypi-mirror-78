# Imports from Django.
from django.db import models


# Imports from other dependencies.
from civic_utils.models import CivicBaseModel


class ExportRecord(CivicBaseModel):
    """A category that races or bodies can be rated into."""

    natural_key_fields = ["label"]

    CUMULATIVE_RECORDS_TYPE = "cumulative-records"
    RACE_RATINGS_TYPE = "race-ratings"
    RATING_DELTAS_TYPE = "rating-deltas"

    RECORD_TYPE_CHOICES = (
        (CUMULATIVE_RECORDS_TYPE, "Cumulative winner records"),
        (RACE_RATINGS_TYPE, "Race ratings"),
        (RATING_DELTAS_TYPE, "Race rating deltas"),
    )

    IN_PROGRESS_STATUS = -1
    SUCCESS_STATUS = 0
    FAIL_STATUS = 1

    STATUS_CHOICES = (
        (IN_PROGRESS_STATUS, "In progress"),
        (SUCCESS_STATUS, "Success"),
        (FAIL_STATUS, "Fail"),
    )

    task_id = models.CharField(max_length=75, unique=True)
    record_type = models.SlugField(
        max_length=25,
        choices=RECORD_TYPE_CHOICES,
        default=CUMULATIVE_RECORDS_TYPE,
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=IN_PROGRESS_STATUS
    )

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.status == self.IN_PROGRESS_STATUS:
            return f"{self.task_id} (in progress)"

        return " ".join(
            [
                f"{self.task_id}",
                f"({self.get_status_display()} in {self.duration}s)",
            ]
        )

    @property
    def duration(self):
        if not self.end_time:
            return None

        duration_delta = self.end_time - self.start_time

        return round(
            duration_delta.seconds + (duration_delta.microseconds / 1000000), 2
        )
