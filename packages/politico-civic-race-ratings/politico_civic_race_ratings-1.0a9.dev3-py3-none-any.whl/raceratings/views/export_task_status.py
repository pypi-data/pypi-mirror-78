# Imports from other dependencies.
from raceratings.models import ExportRecord
from rest_framework import status

# from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Imports from election_loader.
from raceratings.utils.api_auth import CsrfExemptSessionAuthentication
from raceratings.utils.api_auth import TokenAPIAuthentication


class ExportTaskStatusCheckView(APIView):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        failure_content = dict(status_text="Export record not found.")

        if "task_id" not in kwargs:
            return Response(failure_content, status=status.HTTP_404_NOT_FOUND)

        limiting_query = {}
        if "export_type" in kwargs:
            limiting_query["record_type"] = kwargs["export_type"]

        try:
            export_record = ExportRecord.objects.filter(**limiting_query).get(
                task_id=kwargs["task_id"]
            )
        except ExportRecord.DoesNotExist:
            return Response(failure_content, status=status.HTTP_404_NOT_FOUND)

        success_content = dict(
            statusText="One record found",
            record=dict(
                taskID=export_record.task_id,
                recordType=export_record.get_record_type_display(),
                status=export_record.get_status_display(),
                startTime=export_record.start_time,
                endTime=export_record.end_time,
                duration=export_record.duration,
            ),
        )

        return Response(success_content, status=status.HTTP_200_OK)
