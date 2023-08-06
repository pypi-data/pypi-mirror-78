# Imports from Django.
from django.db.models.signals import post_save
from django.dispatch import receiver


# Imports from race_ratings.
from raceratings.celery import bake_all_race_rating_deltas
from raceratings.celery import bake_all_race_ratings
from raceratings.models import BodyRating
from raceratings.models import RaceRating


@receiver(post_save, sender=RaceRating)
def race_rating_save(sender, instance, **kwargs):
    bake_all_race_rating_deltas.apply_async((instance.race.cycle.slug, True))
    bake_all_race_ratings.apply_async((instance.race.cycle.slug, True))


@receiver(post_save, sender=BodyRating)
def body_rating_save(sender, instance, **kwargs):
    pass
    # bake_body_ratings()
