# Imports from other dependencies.
from civic_utils.serializers import CommandLineListSerializer
from civic_utils.serializers import NaturalKeySerializerMixin
from election.models import Race
from geography.models import DivisionLevel
from rest_framework import serializers


# Imports from race_ratings.
from raceratings.models import Category
from raceratings.models import RaceRating
from raceratings.serializers.category import CategorySerializer


CATEGORY_DICT = dict((_.id, _) for _ in Category.objects.all())


class RaceRatingSerializer(
    NaturalKeySerializerMixin, CommandLineListSerializer
):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    class Meta(CommandLineListSerializer.Meta):
        model = RaceRating
        fields = ("pk", "created", "category", "explanation")


class RaceRatingAdminSerializer(CommandLineListSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.category.short_label

    class Meta(CommandLineListSerializer.Meta):
        model = RaceRating
        fields = ("pk", "created", "rating", "explanation")


class RaceDeltaSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    def get_label(self, obj):
        if obj.office.body and obj.office.body.slug == "senate":
            label = "{} {}".format(obj.office.division.label, "Senate")
        else:
            label = obj.office.label

        if obj.special:
            return "{} Special".format(label)
        else:
            return label

    def get_id(self, obj):
        # for easier search
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            postal = obj.office.division.parent.code_components[
                "postal"
            ].lower()
            code = obj.office.division.code
            return "{}-{}".format(postal, code)

        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.slug == DivisionLevel.STATE:
                postal = obj.division.code_components["postal"].lower()
                return "{}-{}".format(postal, "potus")

            postal = obj.division.parent.code_components["postal"].lower()
            return "{}-{}-{}".format(postal, obj.division.code, "potus")

        postal = obj.office.division.code_components["postal"].lower()

        if obj.office.body:
            base = "{}-{}".format(postal, "sen")

            return "{}-{}".format(base, "special") if obj.special else base

        return "{}-{}".format(postal, "gov")

    def get_body(self, obj):
        if obj.office.body:
            return obj.office.body.slug

        return (
            "president"
            if obj.office.division.level.slug == DivisionLevel.COUNTRY
            else "governor"
        )

    def get_state(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return obj.office.division.parent.code
        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.name == DivisionLevel.DISTRICT:
                return obj.division.parent.code
            return obj.division.code
        else:
            return obj.office.division.code

    def get_district(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return "{}-{}".format(
                obj.office.division.parent.code, obj.office.division.code
            )
        elif obj.office.division.level.slug == DivisionLevel.COUNTRY:
            if obj.division.level.name == DivisionLevel.DISTRICT:
                return "{}-{}".format(
                    obj.division.parent.code, obj.division.code
                )

        return None

    class Meta:
        model = Race
        fields = ("label", "id", "body", "state", "district")


class RaceRatingDeltaSerializer(serializers.ModelSerializer):
    day_of_change = serializers.SerializerMethodField()
    race = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    previous_category = serializers.SerializerMethodField()

    def get_day_of_change(self, obj):
        return obj.created.strftime("%Y-%m-%d")

    def get_race(self, obj):
        return RaceDeltaSerializer(obj.race).data

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def get_previous_category(self, obj):
        # ordered_ratings = list(obj.race.ratings.order_by("created"))
        # index = ordered_ratings.index(obj)
        # return CategorySerializer(ordered_ratings[index - 1].category).data
        return (
            CategorySerializer(
                CATEGORY_DICT[obj.most_recent_past_category_id]
            ).data
            if obj.most_recent_past_category_id
            else None
        )

    class Meta:
        model = RaceRating
        fields = (
            "day_of_change",
            "race",
            "category",
            "previous_category",
            "explanation",
        )
