from serializers import Serializer, IntegerField, CharField, BooleanField, ChoiceField
import json


class ExampleSerializer(Serializer):

    CHOICES = ('some', 'choices')

    char_field = CharField()
    int_field = IntegerField(min_value=2, max_value=5)
    bool_field = BooleanField()
    choice_field = ChoiceField(choices=CHOICES)


data = {
    'char_field': 'Some char field',
    'int_field': '3',
    'bool_field': 'false',
    'choice_field': 'choices'
}
serializer = ExampleSerializer(data=data)

print json.dumps(serializer.data)