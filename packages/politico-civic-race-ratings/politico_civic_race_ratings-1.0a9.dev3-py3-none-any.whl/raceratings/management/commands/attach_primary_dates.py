# Imports from Django.
from django.core.management.base import BaseCommand


# Imports from other dependencies.
from election.models import ElectionCycle
from election.models import Race
from elections import ElectionYear
from elections.models.elections import DemocraticPrimaryElection
from elections.models.elections import RepublicanPrimaryElection


# Imports from race_ratings.
from raceratings.constants import ACCEPTED_GOVERNMENT_BODIES
from raceratings.constants import STATE_GOVERNORS_BODY
from raceratings.constants import US_SENATE_BODY
from raceratings.constants import US_HOUSE_BODY
from raceratings.models import DataProfile


class Command(BaseCommand):
    help = (
        "Given a year, record all primary dates for all "
        "general-election races that year (excluding presidential "
        "primaries)."
    )

    bodies_to_create = []

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            required=True,
            help="The year for which we'll be creating races.",
        )

        parser.add_argument(
            "args",
            metavar="government_bodies",
            nargs="*",
            help="".join(
                [
                    "A list of which government bodies should be loaded. ",
                    "These may be any of ",
                    "'{}' or '{}'".format(
                        "', '".join(ACCEPTED_GOVERNMENT_BODIES[:-1]),
                        ACCEPTED_GOVERNMENT_BODIES[-1],
                    )
                    if len(ACCEPTED_GOVERNMENT_BODIES) > 1
                    else "'{}'".format(ACCEPTED_GOVERNMENT_BODIES[0]),
                    ".",
                ]
            ),
        )

    def format_state_primaries(self, primary_election_list):
        formatted_primaries = dict()

        for primary_election in primary_election_list:
            if isinstance(primary_election, DemocraticPrimaryElection):
                formatted_primaries[
                    "dem"
                ] = primary_election.election_date.strftime("%Y-%m-%d")
            elif isinstance(primary_election, RepublicanPrimaryElection):
                formatted_primaries[
                    "gop"
                ] = primary_election.election_date.strftime("%Y-%m-%d")
            else:
                continue

        return formatted_primaries

    def handle(self, *government_bodies, **options):
        # If no government bodies were explicitly stated, create all of them.
        if government_bodies:
            self.bodies_to_create = [
                body
                for body in government_bodies
                if body in ACCEPTED_GOVERNMENT_BODIES
            ]

        if not self.bodies_to_create:
            # self.bodies_to_create = ACCEPTED_GOVERNMENT_BODIES
            self.bodies_to_create = [
                # ELECTORAL_COLLEGE_BODY,
                US_SENATE_BODY,
                US_HOUSE_BODY,
                STATE_GOVERNORS_BODY,
            ]

        self.year = options["year"]

        self.election_year_data = ElectionYear(self.year)
        self.cycle = ElectionCycle.objects.get_or_create(name=self.year)[0]

        # if ELECTORAL_COLLEGE_BODY in self.bodies_to_create:
        #     self.stdout.write(
        #         self.style.MIGRATE_HEADING(
        #             "Creating electoral college races for {}...".format(
        #                 self.year
        #             )
        #         )
        #     )
        #
        #     races_to_modify = Race.objects.filter(
        #         cycle_id=self.cycle.id
        #     ).filter_by_body(Race.ELECTORAL_COLLEGE_CHOICE)

        if US_SENATE_BODY in self.bodies_to_create:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Attaching {} U.S. Senate race primaries...".format(
                        self.year
                    )
                )
            )

            races_to_modify = Race.objects.filter(
                cycle_id=self.cycle.id
            ).filter_by_body(Race.SENATE_CHOICE)

            newly_created = []
            already_existing = []

            for race in races_to_modify:
                state_primaries = self.election_year_data.elections_for_state(
                    race.office.division.code
                ).primaries

                obj, created = DataProfile.objects.get_or_create(
                    race_id=race.id,
                    defaults=dict(
                        data=self.format_state_primaries(state_primaries)
                    ),
                )

                if created:
                    newly_created.append(obj)
                else:
                    already_existing.append(obj)

            self.stdout.write(
                "  ✅   Created {} new {}.".format(
                    len(newly_created),
                    "races" if len(newly_created) != 1 else "race",
                )
            )
            self.stdout.write(
                "  ℹ️   {} {} existed and {} modified.".format(
                    len(already_existing),
                    "races" if len(already_existing) != 1 else "race",
                    "weren't" if len(already_existing) != 1 else "wasn't",
                )
            )
            self.stdout.write("")

        if US_HOUSE_BODY in self.bodies_to_create:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Attaching {} U.S. House race primaries...".format(
                        self.year
                    )
                )
            )

            races_to_modify = Race.objects.filter(
                cycle_id=self.cycle.id
            ).filter_by_body(Race.HOUSE_CHOICE)

            newly_created = []
            already_existing = []

            for race in races_to_modify:
                state_primaries = self.election_year_data.elections_for_state(
                    race.office.division.parent.code
                ).primaries

                obj, created = DataProfile.objects.get_or_create(
                    race_id=race.id,
                    defaults=dict(
                        data=self.format_state_primaries(state_primaries)
                    ),
                )

                if created:
                    newly_created.append(obj)
                else:
                    already_existing.append(obj)

            self.stdout.write(
                "  ✅   Created {} new {}.".format(
                    len(newly_created),
                    "races" if len(newly_created) != 1 else "race",
                )
            )
            self.stdout.write(
                "  ℹ️   {} {} existed and {} modified.".format(
                    len(already_existing),
                    "races" if len(already_existing) != 1 else "race",
                    "weren't" if len(already_existing) != 1 else "wasn't",
                )
            )
            self.stdout.write("")

        if STATE_GOVERNORS_BODY in self.bodies_to_create:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Attaching {} governors race primaries...".format(
                        self.year
                    )
                )
            )

            races_to_modify = Race.objects.filter(
                cycle_id=self.cycle.id
            ).filter_by_body(Race.GOVERNOR_CHOICE)

            newly_created = []
            already_existing = []

            for race in races_to_modify:
                state_primaries = self.election_year_data.elections_for_state(
                    race.office.division.code
                ).primaries

                obj, created = DataProfile.objects.get_or_create(
                    race_id=race.id,
                    defaults=dict(
                        data=self.format_state_primaries(state_primaries)
                    ),
                )

                if created:
                    newly_created.append(obj)
                else:
                    already_existing.append(obj)

            self.stdout.write(
                "  ✅   Created {} new {}.".format(
                    len(newly_created),
                    "races" if len(newly_created) != 1 else "race",
                )
            )
            self.stdout.write(
                "  ℹ️   {} {} existed and {} modified.".format(
                    len(already_existing),
                    "races" if len(already_existing) != 1 else "race",
                    "weren't" if len(already_existing) != 1 else "wasn't",
                )
            )
            self.stdout.write("")
