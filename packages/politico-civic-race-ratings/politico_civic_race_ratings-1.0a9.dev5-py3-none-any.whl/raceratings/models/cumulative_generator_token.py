# Imports from python.
import binascii
import os


# Imports from Django.
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils import timezone


# Imports from other dependencies.
from civic_utils.models import CivicBaseModel
from civic_utils.models import UniqueIdentifierMixin


class CumulativeGeneratorToken(UniqueIdentifierMixin, CivicBaseModel):
    """
    A specific contest in a race held on a specific day.
    """

    natural_key_fields = ["slug"]
    uid_prefix = "cumulative_generator_token"
    default_serializer = (
        "raceratings.serializers.CumulativeGeneratorTokenSerializer"
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=255,
        editable=True,
    )

    key = models.CharField(
        "API key", blank=True, max_length=40, primary_key=True
    )

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """
        **uid field**: :code:`cumulative_generator_token:{description}`
        **identifier**: :code:`<slug uid>__<this uid>`
        """
        self.generate_unique_identifier(always_overwrite_uid=True)

        if not self.key:
            self.key = self.generate_key()
            self.created = timezone.now()

        super(CumulativeGeneratorToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def get_uid_prefix(self):
        return self.uid_prefix

    @property
    def user(self):
        return AnonymousUser
