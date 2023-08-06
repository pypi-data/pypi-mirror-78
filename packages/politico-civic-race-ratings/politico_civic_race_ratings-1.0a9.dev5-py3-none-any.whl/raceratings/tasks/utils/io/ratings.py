# Imports from python.
import codecs
from collections import Counter
from contextlib import closing
import csv
from itertools import groupby
import json


# Imports from Django.
from django.db.models import QuerySet


# Imports from other dependencies.
from civic_utils.utils.aws import get_bucket
from election.models import Race
import requests
from rest_framework.renderers import JSONRenderer
import us


# Imports from race_ratings.
from raceratings.conf import settings
from raceratings.constants import RATING_CATEGORIES
from raceratings.serializers import RaceAPISerializer


BUCKET_NAME = getattr(settings, "AWS_S3_BUCKET")

S3_BUCKET = get_bucket(BUCKET_NAME)

UPLOADED_FILES_ACL = (
    "public-read" if BUCKET_NAME == "interactives.politico.com" else "private"
)

UPLOADED_FILES_CACHE_HEADER = str("max-age=5")

UPLOADED_FILES_PREFIX = "2020-election/data/race-ratings"


def upload_file(destination, contents, mime_type="application/json"):
    s3_destination = f"{UPLOADED_FILES_PREFIX}/{destination}"

    print(">>> Publish data to: ", s3_destination)
    S3_BUCKET.put_object(
        Key=s3_destination,
        ACL=UPLOADED_FILES_ACL,
        Body=contents,
        CacheControl=UPLOADED_FILES_CACHE_HEADER,
        ContentType=mime_type,
    )

    return s3_destination


def load_incumbents(government_body):
    incumbents_for_body = []

    incumbent_list_url = getattr(settings, "INCUMBENT_LIST_URLS", {}).get(
        government_body, None
    )
    if incumbent_list_url:
        with closing(requests.get(incumbent_list_url, stream=True)) as rq:
            reader = csv.DictReader(
                codecs.iterdecode(rq.iter_lines(), "utf-8")
            )

            for row in reader:
                incumbents_for_body.append(row)

    return incumbents_for_body


def create_race_rating_json_for_body(key, race_data, government_body):
    unit_to_count = (
        "votes"
        if government_body == Race.ELECTORAL_COLLEGE_CHOICE
        else "seats"
    )

    body_report = create_race_rating_json(
        key, race_data, override_output_stage=True
    )

    incumbents = load_incumbents(government_body)

    body_report["currentBalance"] = [
        {"party": party_name, unit_to_count: unit_count}
        for party_name, unit_count in Counter(
            incumbent["party"] for incumbent in incumbents
        ).items()
    ]

    if government_body in ["senate", "governors"]:
        if government_body == "senate":
            facing_election = [
                (
                    us.states.lookup(_["office__division__code"]).abbr,
                    _["office__senate_class"],
                )
                for _ in list(
                    race_data.values(
                        "office__division__code", "office__senate_class"
                    )
                )
            ]
            not_facing_election = [
                incumbent
                for incumbent in incumbents
                if (incumbent["state"], incumbent["senate_class"])
                not in facing_election
            ]
        elif government_body == "governors":
            facing_election = [
                us.states.lookup(_["office__division__code"]).abbr
                for _ in list(race_data.values("office__division__code"))
            ]
            not_facing_election = [
                incumbent
                for incumbent in incumbents
                if incumbent["state"] not in facing_election
            ]

        body_report["notFacingElection"] = not_facing_election

    if unit_to_count == "votes":
        electoral_votes_and_categories = sorted(
            list(
                race_data.distinct("uid")
                .order_by("uid")
                .values_list("rating_category", "electoral_votes")
            ),
            key=lambda x: x[0],
        )
        body_report["overallCounts"] = [
            {
                "rating_category": key,
                "seats": sum(
                    [
                        vote_obj[1]
                        for vote_obj in electoral_votes_and_categories
                        if vote_obj[0] == key
                    ]
                ),
            }
            for key in RATING_CATEGORIES
        ]
    elif unit_to_count == "seats":
        races_by_category = sorted(
            list(
                race_data.distinct("uid")
                .order_by("uid")
                .values_list("rating_category", flat=True)
            )
        )
        pre_sorted_counts = {
            key: len(list(group)) for key, group in groupby(races_by_category)
        }
        body_report["overallCounts"] = [
            {
                "rating_category": category,
                "seats": pre_sorted_counts.get(category, 0),
            }
            for category in RATING_CATEGORIES
        ]

    body_report_string = json.dumps(body_report)

    s3_file_location = upload_file(key, body_report_string)

    return s3_file_location


def create_race_rating_json(key, race_data, override_output_stage=False):
    is_list_page = isinstance(race_data, QuerySet)

    if is_list_page:
        data = RaceAPISerializer(race_data, many=True).data
    else:
        data = RaceAPISerializer(race_data).data

    json_string = JSONRenderer().render(data)

    if not is_list_page:
        s3_file_location = upload_file(key, json_string)

        return s3_file_location

    wrapped_json = {"ratings": json.loads(json_string)}

    if override_output_stage:
        return wrapped_json

    wrapped_json_string = json.dumps(wrapped_json)

    s3_file_location = upload_file(key, wrapped_json_string)

    return s3_file_location
