# Imports from other dependencies.
from election.models import Race
from geography.models import DivisionLevel
import us


def NOOP_FN(raw_value):
    return raw_value


def process_state(state_fips):
    return us.states.lookup(state_fips).abbr.lower()


def return_potus(raw_value):
    return "potus"


def return_governor(raw_value):
    return "governor"


government_body_sitemap_parts = {
    "potus_states": {
        "filter_kwargs": {
            "office__body__isnull": True,
            "office__division__level__slug": DivisionLevel.COUNTRY,
            "division__level__slug": DivisionLevel.STATE,
        },
        "data_blueprint": {
            "division__code": {
                "destination_name": "state",
                "transformation": process_state,
            },
            "id": {
                "destination_name": "office",
                "transformation": return_potus,
            },
        },
    },
    "potus_districts": {
        "filter_kwargs": {
            "office__body__isnull": True,
            "office__division__level__slug": DivisionLevel.COUNTRY,
            "division__level__slug": DivisionLevel.DISTRICT,
        },
        "data_blueprint": {
            "division__parent__code": {
                "destination_name": "state",
                "transformation": process_state,
            },
            "division__code": {"destination_name": "district"},
            "id": {
                "destination_name": "office",
                "transformation": return_potus,
            },
        },
    },
    "senate": {
        "filter_kwargs": {"office__body__slug": "senate"},
        "data_blueprint": {
            "office__division__code": {
                "destination_name": "state",
                "transformation": process_state,
            },
            "office__body__slug": {"destination_name": "office"},
            "special": {"destination_name": "isSpecial"},
        },
    },
    "house": {
        "filter_kwargs": {"office__body__slug": "house"},
        "data_blueprint": {
            "office__division__parent__code": {
                "destination_name": "state",
                "transformation": process_state,
            },
            "office__division__code": {"destination_name": "district"},
            "office__body__slug": {"destination_name": "office"},
            "special": {"destination_name": "isSpecial"},
        },
    },
    "governor": {
        "filter_kwargs": {
            "office__body__isnull": True,
            "office__division__level__slug": DivisionLevel.STATE,
        },
        "data_blueprint": {
            "office__division__code": {
                "destination_name": "state",
                "transformation": process_state,
            },
            "id": {
                "destination_name": "office",
                "transformation": return_governor,
            },
        },
    },
}


def generate_sitemap(election_year):
    full_sitemap = []

    for office_slug, office_config in government_body_sitemap_parts.items():
        data_blueprint = office_config.get("data_blueprint", {})

        raw_races_for_office = Race.objects.filter(
            cycle__slug=str(election_year),
            **office_config.get("filter_kwargs", {})
        ).values(*data_blueprint.keys())

        full_sitemap.extend(
            [
                {
                    data_blueprint[raw_field_name]
                    .get("destination_name", raw_field_name): data_blueprint[
                        raw_field_name
                    ]
                    .get("transformation", NOOP_FN)(raw_field_value)
                    for raw_field_name, raw_field_value in race.items()
                }
                for race in raw_races_for_office
            ]
        )

    return full_sitemap
