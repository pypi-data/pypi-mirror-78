import sqlite3
from textwrap import dedent
from typing import Iterator, Sequence, Type, TypeVar
from uuid import uuid4

from ...query import Clause
from .base import Architect, Engine, SelectStatement


class SQLite3Architect(Architect):

    def execute(self, query):
        cursor = self._con.cursor()
        cursor.execute(query)
        return cursor

    def create_model(self, model):
        table_name = model.get_table_name()
        self.execute(f'CREATE TABLE {table_name}(id);')
        for name, field in model.enumerate_fields():
            self.create_field(table_name, field)
        self._con.commit()

    def create_field(self, table_name, field):
        name = field.name
        if name != 'id':
            self.execute(f'ALTER TABLE {table_name} ADD COLUMN {name};')
            self._con.commit()


class SQLite3Clause(Clause):

    CLS = TypeVar('SQLite3Clause', bound='SQLite3Clause')

    def __init__(self, field, operator, value):
        super().__init__(field, operator, value)

    @classmethod
    def from_clause(cls: Type[CLS], clause: Clause) -> CLS:
        return cls(clause.field, clause.operator, clause.value)

    def to_sql(self):
        return f'{self.field} = ?'


class SQLite3Select(SelectStatement):

    def iterate_filters(self) -> Iterator[Clause]:
        for current in self.plan.filters:
            yield SQLite3Clause.from_clause(current)

    def iterate_includes(self) -> Iterator[Clause]:
        for current in self.plan.includes:
            yield SQLite3Clause.from_clause(current)

    def _build_where_clause_part(self, clauses: Sequence[Clause],
                                 operator: str) -> str:
        parts = []
        for current in clauses:
            parts.append(current.to_sql())
            self.append_param(current.value)
        sql = f' {operator} '.join(parts)
        return sql

    def build_where_filters(self):
        filters = list(self.iterate_filters())
        return self._build_where_clause_part(filters, 'AND')

    def build_where_includes(self):
        includes = list(self.iterate_includes())
        return self._build_where_clause_part(includes, 'OR')

    def build_where_clause(self):
        filters = self.build_where_filters()
        includes = self.build_where_includes()
        not_empty = []
        if filters:
            not_empty.append(filters)
        if includes:
            not_empty.append(includes)
        condition = ' OR '.join(not_empty)
        return f'WHERE {condition}'

    def build_fields(self):
        columns = ', '.join(self.plan.columns)
        return columns

    def build_from_clause(self):
        if self.plan.sources:
            sources = ', '.join(self.plan.sources)
            return f'FROM {sources}'
        return ''

    def build_sql(self):
        fields = self.build_fields()
        from_clause = self.build_from_clause()
        where_clause = self.build_where_clause()
        return dedent(f"""
        SELECT {fields}
        {from_clause}
        {where_clause}
        """).strip()


class SQLite3Engine(Engine):

    ddl_class = SQLite3Architect

    def __init__(self, in_memory=False):
        self._in_memory = in_memory
        super().__init__()

    def _get_filename(self):
        if self._in_memory:
            filename = ':memory:'
        else:
            filename = 'albus.db'
        return filename

    def _generate_pk(self, model):
        return uuid4().hex

    def connect(self):
        filename = self._get_filename()
        self._con = sqlite3.connect(filename)

    def cursor(self):
        return self._con.cursor()

    def commit(self):
        self._con.commit()

    def select_query(self, query):
        select = SQLite3Select.from_query(query)
        sql = select.build_sql()
        params = select.params
        cursor = self.cursor()
        cursor.execute(sql, params)
        all_rows = cursor.fetchall()
        cursor.close()
        return all_rows

    def fetch(self, model, pk, fields):
        table = model.get_table_name()
        columns = ', '.join([f.name for f in fields])
        sql = f'SELECT {columns} from {table} WHERE id=?;'
        cursor = self.cursor()
        cursor.execute(sql, [pk])
        row = cursor.fetchone()
        cursor.close()
        values = []
        assert len(row) == len(fields)
        for idx in range(len(fields)):
            current_field = fields[idx]
            current_value = current_field.from_db(row[idx])
            values.append(current_value)
        return values

    def insert(self, model, fields, values):
        pk = self._generate_pk(model)

        names = ['id'] + [f.name for f in fields]
        literals = [pk] + [v for v in values]

        columns = ', '.join(names)
        params = ', '.join(['?'] * len(literals))
        table = model.get_table_name()
        dml = f'INSERT INTO {table} ({columns}) VALUES ({params});'

        cursor = self.cursor()
        cursor.execute(dml, literals)
        self.commit()
        cursor.close()

        return pk

    def update(self, model, fields, values):
        table = model.get_table_name()
        assignments_list = []
        for current_field in fields:
            column_name = current_field.name
            current_assignment = f'\n\t{column_name} = ?'
            assignments_list.append(current_assignment)
        assignments = ','.join(assignments_list)
        dml = f'UPDATE {table} SET {assignments};'

        cursor = self.cursor()
        cursor.execute(dml, values)
        self.commit()
        cursor.close()

    def delete(self, model, pk):
        table = model.get_table_name()
        dml = f'DELETE FROM {table} WHERE id=?;'
        cursor = self.cursor()
        cursor.execute(dml, [pk])
        self.commit()
        cursor.close()
