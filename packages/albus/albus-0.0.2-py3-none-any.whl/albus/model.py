from collections import defaultdict

from .db.engine import SQLite3Engine
from .exceptions import AlbusError
from .field import PrimaryKeyField
from .query import ModelQuery


class BaseModel:

    __fields = defaultdict(dict)
    table_name = None

    def __init__(self, *args, **kwargs):
        for attr_name, field in self.enumerate_fields():
            if attr_name in kwargs:
                setattr(self, attr_name, kwargs[attr_name])

    @classmethod
    def get_table_name(cls):
        table_name = cls.table_name
        if table_name is None:
            table_name = cls.__name__.lower()
        return table_name

    @classmethod
    def register_field(cls, attr_name, field):
        cls.__fields[cls][attr_name] = field

    @classmethod
    def enumerate_fields(cls):
        all_fields = {}
        model_mro = cls._get_model_mro()
        for owner in reversed(model_mro):
            owner_fields = cls.__fields[owner]
            all_fields.update(owner_fields)
        for name, field in all_fields.items():
            yield name, field

    @classmethod
    def _get_model_mro(cls):
        found = []
        for current in cls.mro():
            if issubclass(current, Model):
                found.append(current)
        return found


class Model(BaseModel):

    pk = PrimaryKeyField()

    db_engine = SQLite3Engine(in_memory=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._persisted = False

    @classmethod
    def from_db(cls, **kwargs):
        loaded = cls(**kwargs)
        loaded._persisted = True
        return loaded

    @classmethod
    def new_query(cls) -> ModelQuery:
        return ModelQuery(cls)

    def to_json(self):
        result = {}
        for name, field, value in self.enumerate_fields_values():
            result[field.name] = field.to_json(value)
        return result

    def to_db(self):
        all_fields = []
        all_values = []
        for attr_name, field, value in self.enumerate_fields_values():
            if attr_name != 'pk':
                all_fields.append(field)
                all_values.append(value)
        return all_fields, all_values

    def enumerate_fields_values(self):
        for name, field in type(self).enumerate_fields():
            value = getattr(self, name)
            yield name, field, value

    @classmethod
    def create(cls, **kwargs):
        new = cls(**kwargs)
        new.save()
        return new

    @classmethod
    def get(cls, pk):
        fields = [f for _, f in cls.enumerate_fields()]
        found = cls.db_engine.fetch(cls, pk, fields)
        assert len(fields) == len(found)
        loaded = cls()
        for idx, current_field in enumerate(fields):
            current_value = current_field.from_db(found[idx])
            current_field.__set__(loaded, current_value)
        return loaded

    def destroy(self):
        if not self._persisted:
            raise AlbusError(
                "Cannot Destroy",
                detail="Only persisted records can be destroyed.",
            )
        model = type(self)
        self.db_engine.delete(model, self.pk)

    def save(self):
        model = type(self)
        fields, values = self.to_db()
        if self._persisted:
            self.db_engine.update(model, fields, values)
        else:
            new_identifier = self.db_engine.insert(model, fields, values)
            self.pk = new_identifier
            self._persisted = True
