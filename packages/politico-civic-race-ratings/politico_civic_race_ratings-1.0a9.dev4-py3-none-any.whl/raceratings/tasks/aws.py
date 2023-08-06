# Imports from python.
from itertools import chain
from itertools import groupby
import json
import logging


# Imports from other dependencies.
from celery import shared_task
from election.models import Race
from government.models import Body
from rest_framework.renderers import JSONRenderer


# Imports from race_ratings.
from raceratings.serializers import BodyRatingSerializer

# from raceratings.serializers import RaceRatingFeedSerializer

# from raceratings.utils.aws import defaults
# from raceratings.utils.aws import get_bucket


logger = logging.getLogger("tasks")
