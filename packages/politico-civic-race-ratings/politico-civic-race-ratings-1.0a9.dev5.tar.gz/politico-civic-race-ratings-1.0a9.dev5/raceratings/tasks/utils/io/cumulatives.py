# Imports from other dependencies.
from civic_utils.utils.aws import get_bucket


# Imports from race_ratings.
from raceratings.conf import settings


BUCKET_NAME = getattr(settings, "AWS_S3_BUCKET")

S3_BUCKET = get_bucket(BUCKET_NAME)

UPLOADED_FILES_ACL = (
    "public-read" if BUCKET_NAME == "interactives.politico.com" else "private"
)

UPLOADED_FILES_CACHE_HEADER = str("max-age=5")

UPLOADED_FILES_PREFIX = "2020-election/data/cumulative-rollups"


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
