# Imports from python.
from datetime import datetime
from datetime import time


# Imports from Django.
from django.db.models import DateField
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models.functions import Trunc
from django.utils.timezone import make_aware


# Imports from other dependencies.
from celery import shared_task
from election.models import Race


# Imports from race_ratings.
from raceratings.conf import settings
from raceratings.models import RaceRating
from raceratings.serializers import RaceRatingDeltaSerializer
from raceratings.tasks.utils.io.ratings import UPLOADED_FILES_PREFIX


DELTA_DAYS_PER_PAGE = 5


def generate_body_delta_url(body, page, absolute=False):
    body_prefix = "changelist"
    if body is not None:
        body_prefix = f"{body}/changelist"

    formatted_page = str(page).zfill(3)
    unique_data_path = f"{body_prefix}/page-{formatted_page}.json"

    if not absolute:
        return unique_data_path

    site_root = getattr(settings, "SITE_ROOT", "")
    return f"{site_root}/{UPLOADED_FILES_PREFIX}/{unique_data_path}"


def get_changed_ratings(election_year, government_body):
    if government_body is None:
        filtered_race_ids = Race.objects.filter_by_cycle(
            election_year
        ).values_list("id", flat=True)
    else:
        filtered_race_ids = (
            Race.objects.filter_by_cycle(election_year)
            .filter_by_body(government_body)
            .values_list("id", flat=True)
        )

    rating_start_date = datetime.strptime(
        getattr(settings, "OPEN_DATE", "2019-01-01"), "%Y-%m-%d"
    ).date()

    created_date_threshold = make_aware(
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
        .exclude(created__lt=created_date_threshold)
        .annotate(
            created_day=Trunc("created", "day", output_field=DateField()),
            most_recent_past_category_id=Subquery(
                RaceRating.objects.filter(race_id=OuterRef("race_id"))
                .exclude(created__gte=OuterRef("created"))
                .order_by("-created")
                .values("category_id")[:1]
            ),
        )
        .filter(race_id__in=filtered_race_ids)
        .order_by(
            "-created_day",
            "race__office__division__parent__code",
            "race__office__division__code",
        )
    )


def split_days_into_pages(filtered_ratings):
    days_with_deltas = sorted(
        list(set(filtered_ratings.values_list("created_day", flat=True))),
        reverse=True,
    )

    return [
        days_with_deltas[i : i + DELTA_DAYS_PER_PAGE]
        for i in range(0, len(days_with_deltas), DELTA_DAYS_PER_PAGE)
    ]


def generate_delta_page(
    government_body,
    page_number,
    days_on_page,
    matching_ratings,
    total_page_count,
):
    filename = generate_body_delta_url(government_body, page_number)

    payload = dict(
        count=len(days_on_page),
        next=generate_body_delta_url(government_body, page_number + 1, True)
        if page_number < total_page_count
        else None,
        previous=generate_body_delta_url(
            government_body, page_number - 1, True
        )
        if page_number != 1
        else None,
        results=[],
        perPage=DELTA_DAYS_PER_PAGE,
    )

    for day in days_on_page:
        rating_changes_for_day = matching_ratings.filter(created_day=day)
        payload["results"].append(
            dict(
                day=day.strftime("%Y-%m-%d"),
                ratings=RaceRatingDeltaSerializer(
                    rating_changes_for_day, many=True
                ).data,
            )
        )

    return filename, payload
