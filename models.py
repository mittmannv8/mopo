
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

    __fields = {}

    def __new__(cls, *args, **kwargs):
        new_instance = object.__new__(cls)

        members = zip(cls.__dict__.keys(), cls.__dict__.values())
        cls._attributes = {k: v for k, v in members if getattr(v, 'type', None)}
        cls._attr_state = {}

        for name in cls._attributes.keys():
            try:
                cls.__fields.update({name: 
                getattr(new_instance, name)._set_field_name('__' + name)
            except:
                pass
        return new_instance

    def __init__(self, *args, **kwargs):

        for name in self._attributes.keys():
            print(name)
            init_param = kwargs.pop(name, None)
            if init_param and name in self._attributes.keys():
                print('init_param')
                value = init_param
            else:
                print('default')
                value = self._attributes.get(name).field_default
            setattr(self, name, value)

