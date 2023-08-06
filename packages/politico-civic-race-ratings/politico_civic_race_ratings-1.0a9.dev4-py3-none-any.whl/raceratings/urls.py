# Imports from Django.
from django.urls import include
from django.urls import path
from django.urls import re_path


# Imports from other dependencies.
from rest_framework.routers import DefaultRouter


# Imports from race_ratings.
from raceratings.views import CumulativeWinnerExportView
from raceratings.views import ExportTaskStatusCheckView
from raceratings.views import Home
from raceratings.views import RacePage
from raceratings.views import RaceRatingsExportView
from raceratings.views import RatingDeltasExportView
from raceratings.views import RatingsEditor
from raceratings.viewsets import BodyRatingsViewSet
from raceratings.viewsets import RaceRatingsAPIViewSet
from raceratings.viewsets import RaceRatingsFilterViewSet
from raceratings.viewsets import RaceRatingsFeedViewSet
from raceratings.viewsets import RatingAdminView
from raceratings.viewsets import RaceRatingsViewSet
from raceratings.viewsets import RaceRatingDeltasViewSet


app_name = "race_ratings"


router = DefaultRouter()
router.register(r"race-ratings/(?P<year>\d{4})", RaceRatingsViewSet)
router.register(
    r"race-ratings/deltas/(?P<year>\d{4})", RaceRatingDeltasViewSet
)


urlpatterns = [
    re_path(r"^api/v2/", include(router.urls), name="actual-api"),
    path(Home.path, Home.as_view(), name=Home.name),
    re_path(RacePage.path, RacePage.as_view(), name=RacePage.name),
    path("editor/", RatingsEditor.as_view(), name="editor-ui"),
    path(
        "cumulative-summaries/export/",
        CumulativeWinnerExportView.as_view(),
        name="cumulative-summaries-export",
    ),
    path(
        "per-race-ratings/export/",
        RaceRatingsExportView.as_view(),
        name="ratings-and-deltas-export",
    ),
    path(
        "rating-deltas/export/",
        RatingDeltasExportView.as_view(),
        name="ratings-and-deltas-export",
    ),
    path(
        "task-status-check/<slug:task_id>/",
        ExportTaskStatusCheckView.as_view(),
        name="export-task-status",
    ),
    path(
        "task-status-check/<slug:export_type>/<slug:task_id>/",
        ExportTaskStatusCheckView.as_view(),
        name="export-task-status-by-type",
    ),
    re_path(
        r"^api/ratings/$",
        RaceRatingsAPIViewSet.as_view(),
        name="raceratings_api_ratings-api",
    ),
    re_path(
        r"^api/filters/$",
        RaceRatingsFilterViewSet.as_view(),
        name="raceratings_api_filters-api",
    ),
    re_path(
        r"^api/feed/$",
        RaceRatingsFeedViewSet.as_view(),
        name="raceratings_api_feed-api",
    ),
    re_path(
        r"^api/body-ratings/$",
        BodyRatingsViewSet.as_view(),
        name="raceratings_api_body-ratings-api",
    ),
    re_path(
        r"^api/admin/ratings/$",
        RatingAdminView.as_view(),
        name="raceratings_api_ratings-admin",
    ),
]
