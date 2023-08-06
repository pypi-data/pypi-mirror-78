# Imports from python.
import json


# Imports from other dependencies.
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Imports from race-ratings.
from raceratings.celery import bake_all_race_ratings
from raceratings.utils.api_auth import CsrfExemptSessionAuthentication
from raceratings.utils.api_auth import TokenAPIAuthentication
from raceratings.views.mixins.election_year import ElectionYearMixin


class RaceRatingsExportView(ElectionYearMixin, APIView):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get_context_data(self, *args, **kwargs):
        data = super(RaceRatingsExportView, self).get_context_data(
            *args, **kwargs
        )
        return data

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)

        task_args = dict(
            election_year=self.get_election_year(
                json_body.get("electionYear", "")
            ),
            bodies=json_body.get("bodies", []),
            include_special_elections=json_body.get(
                "includeSpecialElections", "False"
            ).lower()
            == "true",
        )

        if task_args.get("election_year", None) is None:
            raise APIException(
                f"Invalid election cycle '{json_body.get('electionYear')}'"
            )

        export_task = bake_all_race_ratings.apply_async((task_args,))

        # A separate process will be responsible for pulling race and candidate
        # metadata back _out_ of Civic when it's ready, and having this task ID
        # will help that process determine when it can start that step.
        task_id = export_task.id

        success_message = (
            "Baking race ratings, including special elections."
            if task_args.get("include_special_elections", False) is True
            else "Baking race ratings, NOT including special elections."
        )

        content = dict(
            status=202,
            taskID=task_id,
            receivedBody=json_body,
            message=success_message,
            requestedBy=request.auth.uid,
        )

        return Response(content, status=status.HTTP_202_ACCEPTED)
