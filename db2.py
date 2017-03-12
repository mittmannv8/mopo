import sqlite3


class Field:
    """Represent a property type for model items."""

    def __init__(self, default=None):
        self.field_name = ''
        self.default = default if default else self

    def _set_field_name(self, name):
        self.field_name = name

    def _validate(self, value):
        return isinstance(value, self.type)

    def _normalize(self, value):
        return value

    def __get__(self, instance, cls):
        print('get')
        return getattr(instance, self.field_name, self.default)

    def __set__(self, instance, value):
        print('set')
        if self._validate(value):
            setattr(instance, self.field_name, self._normalize(value))
        else:
            raise TypeError('Must be a {}'.format(self.type))

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class CharField(Field):
    def __init__(self, *args, **kwargs):
        self.type = str
        self.max_length = kwargs.pop('max_length', None)

        if not self.max_length:
            raise ValueError('You must set the max_length')

        super().__init__(*args, **kwargs)

    def _validate(self, value):
        if len(value) > self.max_length:
            raise ValueError('Lenght larger than specified ({} characters)'.format(
                self.max_length))

        return True

    def _normalize(self, value):
        return str(value)


class IntegerField(Field):
    def __init__(self, *args, **kwargs):
        self.type = int
        super().__init__(*args, **kwargs)


class BooleanField(Field):
    def __init__(self, *args, **kwargs):
        self.type = bool
        super().__init__(*args, **kwargs)

    def _validate(self, value):
        return True if isinstance(value, bool) or value in (0, 1) else False

    def _normalize(self, value):
        return bool(value)


class Model(object):
    """Represent an instance of model/table.

    >>> class User(Model):
    ...     username = CharField(max_legth=50)
    ...     age = IntegerField()

    >>> user = User(username="Joe", age=30)
    >>> user.save()
    >>> user.username
    ... Joe
    """

    def __new__(cls, *args, **kwargs):
        new_instance = object.__new__(cls)

        members = zip(cls.__dict__.keys(), cls.__dict__.values())
        cls._attributes = {k: v for k, v in members if getattr(v, 'type', None)}

        for name in cls._attributes.keys():
            getattr(new_instance, name)._set_field_name('_' + name)
            init_param = kwargs.pop(name, None)
            if init_param and name in cls._attributes.keys():
                print('Set value to ' + name)
                setattr(new_instance, name, init_param)

        return new_instance

    def save(self):
        raise NotImplementedError('')



class Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.__connect_db()

    def __connect_db(self):
        self._connection = sqlite3.connect(self.db_name)
        self._cursor = self._connection.cursor()

    def create_table(self, model):
        cur = self._cursor
        model = model()
        print(model.__dict__)


class QuerySet:
    """Represent a collection of Models."""

    def __init__(self):
        pass

    def filter(self, **kwargs):
        pass

    def get(self, **kwargs):
        pass


class ModelField(Model):
    nome = CharField(max_length=255)
    idade = IntegerField()
    staff = BooleanField()


db = Database(':memory:')
db.create_table(ModelField)
