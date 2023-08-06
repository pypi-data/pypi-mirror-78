# Imports from other dependencies.
from election.models import ElectionCycle


class ElectionYearMixin(object):
    def get_election_year(self, raw_election_year):
        try:
            matching_cycle = ElectionCycle.objects.get(slug=raw_election_year)
        except ElectionCycle.DoesNotExist:
            return None

        return matching_cycle.slug
