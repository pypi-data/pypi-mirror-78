"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

# Imports from Django.
from django.conf import settings as project_settings


class Settings:
    pass


Settings.AWS_ACCESS_KEY_ID = getattr(
    project_settings,
    "RACE_RATINGS_AWS_ACCESS_KEY_ID",
    getattr(project_settings, "CIVIC_AWS_ACCESS_KEY_ID", ""),
)

Settings.AWS_SECRET_ACCESS_KEY = getattr(
    project_settings,
    "RACE_RATINGS_AWS_SECRET_ACCESS_KEY",
    getattr(project_settings, "CIVIC_AWS_SECRET_ACCESS_KEY", ""),
)


Settings.AWS_S3_BUCKET = getattr(
    project_settings,
    "RACE_RATINGS_AWS_S3_BUCKET",
    getattr(project_settings, "CIVIC_UTILS_AWS_S3_BUCKET", ""),
)

Settings.INCUMBENT_LIST_BASE_PATH = getattr(
    project_settings, "RACE_RATINGS_INCUMBENT_LIST_BASE_PATH", None
)

Settings.INCUMBENT_LIST_URLS = (
    {
        "senate": f"{Settings.INCUMBENT_LIST_BASE_PATH}/us-senate.csv",
        "house": f"{Settings.INCUMBENT_LIST_BASE_PATH}/us-house.csv",
        "governors": f"{Settings.INCUMBENT_LIST_BASE_PATH}/governors.csv",
    }
    if Settings.INCUMBENT_LIST_BASE_PATH
    else {}
)

Settings.SITE_ROOT = (
    "https://www.politico.com"
    if Settings.AWS_S3_BUCKET == "interactives.politico.com"
    else f"http://{Settings.AWS_S3_BUCKET}.s3.amazonaws.com"
)

Settings.OPEN_DATE = getattr(
    project_settings, "RACE_RATINGS_OPEN_DATE", "2019-10-22"
)

Settings.SCRATCH_FILE_DIR = getattr(
    project_settings,
    "RACE_RATINGS_SCRATCH_FILE_DIR",
    getattr(project_settings, "PROJECT_ROOT", ""),
)


settings = Settings
