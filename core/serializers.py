from rest_framework import serializers

from core.models import Input, Data, DateTimeElement, SelectElement, SubForm
from core.sub_form_fields import get_related_fields
from .element_types import INPUT, SELECT, DATE, DATETIME, RADIO, RANGE, CHECKBOX, TIME


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class InputRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ['pk', 'value']


class SelectElementRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectElement
        fields = ['pk', 'value', 'data']


class DateTimeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = ['pk', 'value']


# map of element types to their serializers
_serializers = {
    INPUT: {'retrieve': InputRetrieveSerializer},
    DATETIME: {'retrieve': DateTimeRetrieveSerializer},
    SELECT: {'retrieve': SelectElementRetrieveSerializer}
}


class SubFormRetrieveSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField()

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'fields']

    def get_fields(self):
        _fields = get_related_fields(self.instance)
        _fields_data = []

        for field in _fields:
            _Serializer = _serializers.get(field.type).get('retrieve')
            _field_data = _Serializer(instance=field).data
            _fields_data.append(_field_data)

        return _fields_data
