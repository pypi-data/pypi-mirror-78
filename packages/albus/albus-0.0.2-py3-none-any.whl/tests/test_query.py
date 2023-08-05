from unittest import TestCase

from albus.field import IntegerField, StringField
from albus.query import Clause, Query


class BaseQueryTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query = None

    @property
    def query(self) -> Query:
        if self._query is None:
            self._query = Query()
            self.addCleanup(self.cleanupQuery)
        return self._query

    def cleanupQuery(self):
        if self._query is not None:
            self._query = None

    def assertPlanFiltersEqual(self, expected):
        got = self.query.get_plan()
        self.assertEqual(expected, got.filters)

    def assertPlanIncludesEqual(self, expected):
        got = self.query.get_plan()
        self.assertEqual(expected, got.includes)

    def assertHasNestedFilters(self, expected):
        got = self.query.get_plan()
        all_nested = got.nested_filters + got.nested_includes
        known_filters = []
        for current_nested in all_nested:
            known_filters.append(current_nested.filters)
        self.assertIn(expected, known_filters, 'Nested filter not found')

    def assertHasNestedIncludes(self, expected):
        got = self.query.get_plan()
        all_nested = got.nested_filters + got.nested_includes
        known_includes = []
        for current_nested in all_nested:
            known_includes.append(current_nested.includes)
        self.assertIn(expected, known_includes, 'Nested include not found')


class SimpleQueryTest(BaseQueryTest):

    def setUp(self):
        self.title_field = StringField()
        self.rank_field = IntegerField()

    def test_filter_equals(self):
        self.query.filter_equals(self.title_field, 'Some Book')
        self.assertPlanFiltersEqual([Clause(self.title_field, 'equals', 'Some Book')])

    def test_filter_with_include(self):
        self.query.filter_equals(self.title_field, 'Top Book')
        self.query.include_less(self.rank_field, 10)
        self.assertPlanFiltersEqual([Clause(self.title_field, 'equals', 'Top Book')])
        self.assertPlanIncludesEqual([Clause(self.rank_field, 'less', 10)])


class NestedQueryTest(BaseQueryTest):

    def setUp(self):
        self.maxDiff = None
        self.title_field = StringField()
        self.rank_field = IntegerField()

    def test_verbose_range(self):
        nested = Query()
        nested.include_greater(self.title_field, 'A')
        nested.include_equals(self.title_field, 'A')
        self.query.filter_query(nested)
        self.query.filter_less(self.title_field, 'B')
        self.assertHasNestedIncludes([
            Clause(self.title_field, 'greater', 'A'),
            Clause(self.title_field, 'equals', 'A')],
        )
        self.assertPlanFiltersEqual([Clause(self.title_field, 'less', 'B')])
