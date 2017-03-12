
class BaseField(object):
    """Base of Fields types."""

    type = type
    __field_name = ''
    field_default = None

    def __init__(self, default=None):
        self.default = default if default else self.field_default

    def _set_field_name(self, name):
        """Define """
        self.__field_name = name

    def validate(self, value):
        """Method used for validate the field value.
        This method can be override if necessary other
        validation istead of default type validation."""
        if value is None:
            return True
        return isinstance(value, self.type)

    def normalize(self, value):
        """Normalize value to save correctly on db."""
        return self.type(value)

    def __get__(self, instance, cls):
        print('get')
        print(self.__field_name)
        if not self.__field_name:
            return self
        state = getattr(instance, '_attrs_state')
        return state.get(self.__field_name, self.default)

    def __set__(self, instance, value):
        print('set')
        if self.validate(value):
            state = getattr(instance, '_attrs_state')
            print(self.__field_name)
            state.update({self.__field_name: value})
            setattr(instance, '_attrs_state', state)
        else:
            raise TypeError('Must be {}'.format(self.type))


class CharField(BaseField):
    """Char field type"""

    def __init__(self, *args, **kwargs):
        self.type = str
        self.field_default = ''
        self.max_length = kwargs.pop('max_length', None)

        if not self.max_length:
            raise ValueError('You must set max_length for CharField')

        super().__init__(*args, **kwargs)

    def validate(self, value):
        if len(value) > self.max_length and value is not None:
            raise ValueError('Lenght larger than specified ({} characters)'.format(
                self.max_length))
        return True


class IntegerField(BaseField):
    """Integer field type"""

    def __init__(self, *args, **kwargs):
        self.type = int
        super().__init__(*args, **kwargs)


class BooleanField(BaseField):
    """Boolean field type"""

    def __init__(self, *args, **kwargs):
        self.type = bool
        super().__init__(*args, **kwargs)
