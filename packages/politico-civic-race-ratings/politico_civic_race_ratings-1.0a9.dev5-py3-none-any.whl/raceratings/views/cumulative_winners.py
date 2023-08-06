# Imports from python.
import json


# Imports from other dependencies.
from raceratings.models import ExportRecord
from rest_framework import status

# from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Imports from election_loader.
from raceratings.celery import bake_all_winner_summaries
from raceratings.utils.api_auth import CsrfExemptSessionAuthentication
from raceratings.utils.api_auth import TokenAPIAuthentication


class CumulativeWinnerExportView(APIView):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)

        export_task = bake_all_winner_summaries.apply_async((json_body,))

        # A separate process will be responsible for pulling race and candidate
        # metadata back _out_ of Civic when it's ready, and having this task ID
        # will help that process determine when it can start that step.
        task_id = export_task.id

        reports_pluralized_suffix = (
            "" if len(json_body["bodies"]) == 1 else "s"
        )

        bodies_pluralized = (
            "body" if len(json_body["bodies"]) == 1 else "bodies"
        )

        content = dict(
            status=202,
            taskID=task_id,
            receivedBody=json_body,
            message=" ".join(
                [
                    "Baking cumulative winner",
                    f"report{reports_pluralized_suffix}",
                    f"for {len(json_body['bodies'])}",
                    f"government {bodies_pluralized}.",
                ]
            ),
            requestedBy=request.auth.uid,
        )

        return Response(content, status=status.HTTP_202_ACCEPTED)
