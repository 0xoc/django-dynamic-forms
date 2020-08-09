from rest_framework import serializers

from core.models import Input, Data, DateTimeElement, SelectElement, SubForm
from core.sub_form_fields import get_related_fields
from .element_types import INPUT, SELECT, DATE, DATETIME, RADIO, RANGE, CHECKBOX, TIME

base_fields = ['pk', 'title', 'type', 'filters', 'order']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class InputRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = base_fields


class SelectElementRetrieveSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = SelectElement
        fields = base_fields + ['data', ]


class DateTimeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = base_fields


# map of element types to their serializers
_serializers = {
    INPUT: {'retrieve': InputRetrieveSerializer},
    DATETIME: {'retrieve': DateTimeRetrieveSerializer},
    SELECT: {'retrieve': SelectElementRetrieveSerializer}
}


class SubFormRetrieveSerializer(serializers.ModelSerializer):
    elements = serializers.SerializerMethodField()

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'elements']

    @staticmethod
    def get_elements(instance):
        _fields = get_related_fields(instance)
        _fields_data = []

        for field in _fields:
            _Serializer = _serializers.get(field.type).get('retrieve')
            _field_data = _Serializer(instance=field).data
            _fields_data.append(_field_data)

        return _fields_data


class SubFormRawCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description']


class SubFormCreateSerializer(serializers.ModelSerializer):
    elements = serializers.JSONField()

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'elements']

    def create(self, validated_data):
        print(validated_data.get('elements'))
