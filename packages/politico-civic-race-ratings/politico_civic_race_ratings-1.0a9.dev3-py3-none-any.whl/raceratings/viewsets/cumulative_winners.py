# Imports from python.
import json


# Imports from other dependencies.
from rest_framework import status
# from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Imports from election_loader.
from raceratings.celery import bake_all_winner_summaries
from raceratings.utils.api_auth import CsrfExemptSessionAuthentication
from raceratings.utils.api_auth import TokenAPIAuthentication


class ElectionYearMixin(object):
    pass
    # def get_queryset(self):
    #     """
    #     Returns a queryset of all states holding a non-special election on
    #     a date.
    #     """
    #     try:
    #         date = ElectionDay.objects.prefetch_related(
    #             "election_events",
    #             "election_events__division",
    #             "election_events__division__level",
    #         ).get(date=self.kwargs["date"])
    #     except Exception:
    #         raise APIException(
    #             "No elections on {}.".format(self.kwargs["date"])
    #         )
    #
    #     elections_for_day = date.election_events.filter()
    #
    #     division_ids = []
    #     if len(elections_for_day) > 0:
    #         for event in date.election_events.all():
    #             if event.division.level.name == DivisionLevel.STATE:
    #                 division_ids.append(event.division.uid)
    #             elif event.division.level.name == DivisionLevel.VOTERS_ABROAD:
    #                 division_ids.append(event.division.uid)
    #             elif event.division.level.name == DivisionLevel.DISTRICT:
    #                 division_ids.append(event.division.parent.uid)
    #
    #     return Division.objects.select_related("level").filter(
    #         uid__in=division_ids
    #     )
    #
    # def get_serializer_context(self):
    #     """Adds ``election_day`` to serializer context."""
    #     context = super(StateMixin, self).get_serializer_context()
    #     context["election_date"] = self.kwargs["date"]
    #     return context


class CumulativeWinnerExportView(ElectionYearMixin, APIView):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)

        export_task = bake_all_winner_summaries.delay(json_body)

        # A separate process will be responsible for pulling race and candidate
        # metadata back _out_ of Civic when it's ready, and having this task ID
        # will help that process determine when it can start that step.
        task_id = export_task.id

        reports_pluralized_suffix = '' if len(json_body.bodies) == 1 else 's'
        bodies_pluralized = 'body' if len(json_body.bodies) == 1 else 'bodies'

        content = {
            "status": 202,
            "task_id": task_id,
            "received_body": json_body,
            "message": " ".join([
                f"Baking cumulative winner report{reports_pluralized_suffix}",
                f"for {len(json_body.bodies)}",
                f"government {bodies_pluralized}.",
            ]),
            "requested_by": request.auth.uid,
        }

        return Response(content, status=status.HTTP_202_ACCEPTED)


class CumulativeWinnerExportView(ElectionYearMixin, APIView):
    authentication_classes = [
        CsrfExemptSessionAuthentication,
        TokenAPIAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # json_body = json.loads(request.body)
        print("RQ")
        print(request)
        print()

        content = {
            "asdf": "9989",
        }

        return Response(content, status=status.HTTP_202_ACCEPTED)
