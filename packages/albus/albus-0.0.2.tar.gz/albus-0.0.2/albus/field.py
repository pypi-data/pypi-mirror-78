from . import db


class BaseField:

    def __init__(self, default=None, name=None):
        self.__data = {}
        self.attr_name = None
        self.name = name
        self.default = default

    def __set_name__(self, owner, name):
        self.owner = owner
        self.attr_name = name
        if self.name is None:
            self.name = name
        owner.register_field(name, self)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self.__data.get(obj, self.default)

    def __set__(self, obj, value):
        prepared = self.to_internal(value)
        self.__data[obj] = prepared

    def to_internal(self, value):
        return value


class Field(BaseField):

    db_type = None

    def to_json(self, value):
        return value

    def from_db(self, value):
        return value

    def to_internal(self, value):
        return super().to_internal(value)


class PrimaryKeyField(Field):

    db_type = db.IntegerType()

    def __init__(self):
        super().__init__(name='id')


class IntegerField(Field):

    db_type = db.IntegerType()


class StringField(Field):

    db_type = db.StringType()
