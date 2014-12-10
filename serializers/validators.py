from .exceptions import ValidationException
from urlparse import urlparse


class BaseValidator(object):

    def validate(self, *args, **kwargs):
        raise NotImplementedError


class RequiredValidator(BaseValidator):

    message = 'This value is required.'

    def __init__(self, required):
        self.required = required

    def validate(self, value):
        if self.required and value is None:
            raise ValidationException(self.message)


class MinValueValidator(BaseValidator):

    message = 'The value has to be greater than {}'

    def __init__(self, min_value):
        self.min_value = min_value

    def validate(self, value):
        if value is not None and int(value) < int(self.min_value):
            raise ValidationException(self.message.format(self.min_value))


class MaxValueValidator(BaseValidator):

    message = 'The value has to be lower than {}'

    def __init__(self, max_value):
        self.max_value = max_value

    def validate(self, value):
        if value is not None and int(value) > int(self.max_value):
            raise ValidationException(self.message.format(self.max_value))


class MinLengthValidator(BaseValidator):

    message = 'The value has to be greater than {} characters'

    def __init__(self, min_value):
        self.min_value = min_value

    def validate(self, value):
        if value is not None and len(value) < self.min_value:
            raise ValidationException(self.message.format(self.min_value))


class MaxLengthValidator(BaseValidator):

    message = 'The value has to be lower than {} characters'

    def __init__(self, max_value):
        self.max_value = max_value

    def validate(self, value):
        if value is not None and len(value) > self.max_value:
            raise ValidationException(self.message.format(self.max_value))


class BooleanValidator(BaseValidator):

    message = 'The value is not a valid boolean value'

    def __init__(self):
        pass

    def validate(self, value):
        if value is not None and not isinstance(value, bool):
            if value not in ('true', 'True', '1', 'false', 'False', '0'):
                raise ValidationException(self.message)


class URLValidator(BaseValidator):

    message = 'The value is not a valid URL'

    def __init__(self):
        pass

    def validate(self, value):
        if value is not None and urlparse(value).scheme == '':
            raise ValidationException(self.message)


class ChoiceValidator(BaseValidator):

    message = 'The value is not in the list of possible choices: {}'

    def __init__(self, choices):
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise ValidationException(self.message)