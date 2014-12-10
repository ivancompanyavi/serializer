from collections import OrderedDict
from fields import Field


def _get_declared_fields(bases, attrs):
    """
    Create a list of serializer field instances from the passed in 'attrs',
    plus any fields on the base classes (in 'bases').

    Note that all fields from the base classes are used.
    """
    fields = [(field_name, attrs.pop(field_name))
              for field_name, obj in list(attrs.iteritems())
              if isinstance(obj, Field)]
    fields.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another Serializer, add that Serializer's
    # fields.  Note that we loop over the bases in *reverse*. This is necessary
    # in order to maintain the correct order of fields.
    for base in bases[::-1]:
        if hasattr(base, 'base_fields'):
            fields = list(base.base_fields.items()) + fields

    return OrderedDict(fields)


class BaseSerializer(Field):

    def __init__(self, data=None, many=False, *args, **kwargs):
        self._data = data
        self.many = many
        self._errors = []

        super(BaseSerializer, self).__init__(*args, **kwargs)

    @property
    def data(self):
        """
        Main method of the class. It returns the representation of the serializer with OrderDict.
        :return:
        """
        element_result = []
        self._data = self._data or {}
        if not self.many:
            self._data = [self._data]
        for field_value in self._data:
            result = OrderedDict()
            for field_name, field in self.base_fields.items():
                if hasattr(field_value, 'get'):
                    value = field_value.get(field_name, None)
                    field = self.initialize_field(field, field_name, value)
                    if field.required or value:
                        errors = field.validate()
                        if errors:
                            self._errors.append({field_name: errors})
                        else:
                            result[field_name] = field.to_native()
                else:
                    self._errors.append('The field value \'%s\' has to be a dictionary' % str(field_value))
            element_result.append(result)
        if not self.many:
            element_result = element_result[0]

        if self._errors:
            return self._errors
        else:
            return element_result

    def initialize_field(self, field, field_name, field_value):
        field._name = field_name
        field._value = field_value
        if isinstance(field, BaseSerializer):
            field._data = field._value
        return field

    def to_native(self):
        return self.data


class SerializerMetaclass(type):
    """
    This class is needed to know which fields a serializer has
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_fields'] = _get_declared_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)


class Serializer(BaseSerializer):

    __metaclass__ = SerializerMetaclass


