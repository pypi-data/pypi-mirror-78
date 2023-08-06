# Imports from Django.
from django.db.models import Q


# Imports from other dependencies.
from django_filters import rest_framework as filters
from election.models import Race
from geography.models import DivisionLevel
from government.models import Jurisdiction
from rest_framework.views import APIView
import us


FED_GOVT_ID = (
    Jurisdiction.objects.filter(name="U.S. Federal Government")
    .values_list("id", flat=True)
    .get()
)


class RaceRatingsFilters(filters.FilterSet):
    BODY_CHOICES = Race.BODY_CHOICES

    STATE_CHOICES = [
        *[(_.abbr.lower(), _.name) for _ in us.states.STATES],
        *[(_.name.lower(), _.name) for _ in us.states.STATES],
        *[(_.fips, _.name) for _ in us.states.STATES],
    ]

    state = filters.ChoiceFilter(
        method="filter_by_state", choices=STATE_CHOICES
    )
    type = filters.ChoiceFilter(
        method="filter_by_office_type", choices=BODY_CHOICES
    )

    def filter_by_state(self, queryset, name, state_value):
        return queryset.filter_by_state(state_value)

    def filter_by_office_type(self, queryset, name, value):
        return queryset.filter_by_body(value)

    class Meta:
        model = Race
        fields = ["state", "type"]
