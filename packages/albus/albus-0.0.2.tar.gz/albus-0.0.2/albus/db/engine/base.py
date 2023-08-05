from typing import Any, List, Type, TypeVar

from ...query import Plan, Query


class Architect:

    def __init__(self, con):
        assert con is not None, "Architect needs a connection"
        self._con = con


class SelectStatement:

    CLS = TypeVar('SelectStatement', bound='SelectStatement')

    def __init__(self, query_plan):
        self._plan = query_plan
        self._params = []

    @classmethod
    def from_query(cls: Type[CLS], query: Query) -> CLS:
        query_plan = query.get_plan()
        return cls(query_plan)

    @property
    def plan(self) -> Plan:
        return self._plan

    @property
    def params(self) -> List[Any]:
        return self._params

    def append_param(self, value):
        self._params.append(value)

    def build_where_clause(self):
        raise NotImplementedError()


class Engine:

    ddl_class = None

    def __init__(self):
        self._con = None
        self._ddl = None
        self.connect()

    @property
    def ddl(self):
        if self._ddl is None:
            self._ddl = type(self).ddl_class(self._con)
        return self._ddl

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        if self._con is not None:
            self._con.close()
        self._con = None
