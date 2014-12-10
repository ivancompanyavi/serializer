from .validators import RequiredValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from .validators import BooleanValidator, URLValidator, ChoiceValidator
from .exceptions import ValidationException


class Field(object):
    """
    Base field.
    It has the common features a Field has.
    """

    creation_counter = 0
    default = None

    def __init__(self, required=True):
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1
        self.required = required

        self.validators = []

        self.validators.append(RequiredValidator(required))

        self._name = None
        self._value = None

    def validate(self):
        """
        Validation method. It goes through all the validators of the field and checks if it accomplishes all of them.
        If it doesn't, it returns those errors.
        :return: The list of validator errors. Empty list if there are no errors.
        """
        errors = []
        for validator in self.validators:
            try:
                validator.validate(self._value)
            except ValidationException as e:
                errors.append(e.message)
        return errors

    def to_native(self):
        """
        Method that returns the native version of the input. I.E: an IntegerField with '1' as input, it will return the
        integer version of it, that is int('1')
        :return: The native version of the value
        """
        return self._value or self.default


class CharField(Field):
    """
    Field for characters. It differs from common fields in some extra validators and some options like min_length and
    max_length for filtering the input
    """

    default = ''

    def __init__(self, min_length=None, max_length=None, *args, **kwargs):

        super(CharField, self).__init__(*args, **kwargs)

        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))


class IntegerField(Field):
    """
    Field for integer values. It checks if the input is an integer and has optional filters like min_value of max_value
    """

    default = 0

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):

        super(IntegerField, self).__init__(*args, **kwargs)

        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))
        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))

    def to_native(self):
        return int(self._value)


class BooleanField(Field):
    """
    Field for boolean values. It checks if the input is a boolean.
    """
    default = False

    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)

        self.validators.append(BooleanValidator())

    def to_native(self):
        if isinstance(self._value, bool):
            return self._value
        if self._value in ('true', 'True', '1'):
            return True
        if self._value in ('false', 'False', '0'):
            return False
        return bool(self._value)


class URLField(Field):
    """
    Field for URL values. It checks if the input is a valid URL
    """
    default = ''

    def __init__(self, *args, **kwargs):
        super(URLField, self).__init__(*args, **kwargs)

        self.validators.append(URLValidator())


class ChoiceField(Field):
    """
    Choice field. You can pass it an array of choices and the field will check if the input value is in those choices.
    """

    def __init__(self, choices=(), *args, **kwargs):
        super(ChoiceField, self).__init__(*args, **kwargs)

        self.validators.append(ChoiceValidator(choices))
