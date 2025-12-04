from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, matcher= All()):
        self._matcher = matcher

    def build(self):
        return self._matcher

    def plays_in(self, team):
        matcher = QueryBuilder(And(self._matcher, PlaysIn(team)))
        return matcher

    def has_at_least(self, value, attr):
        matcher = QueryBuilder(And(self._matcher, HasAtLeast(value, attr)))
        return matcher

    def has_fewer_than(self, value, attr):
        matcher = QueryBuilder(And(self._matcher, HasFewerThan(value, attr)))
        return matcher
    
    def one_of(self, *matchers):
        matcher = QueryBuilder(And(self._matcher, Or(*matchers)))
        return matcher
    
