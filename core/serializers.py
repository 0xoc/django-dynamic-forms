from rest_framework import serializers

from core.models import Input, Data, DateTimeElement, SelectElement, SubForm, Element
from core.sub_form_fields import get_related_fields
from .element_types import INPUT, SELECT, DATE, DATETIME, RADIO, RANGE, CHECKBOX, TIME

base_fields = ['pk', 'title', 'type', 'value', 'filters', 'order']
abstract_element_fields = ['pk', 'title', 'type', 'order', 'sub_form']
base_element_fields = abstract_element_fields + ['value', ]


class ElementCreteSerializer(serializers.ModelSerializer):
    """Abstract element serializer"""

    class Meta:
        model = Element
        fields = abstract_element_fields
        abstract = True


class DataSerializer(serializers.ModelSerializer):
    """Element Extra data CRUD serializer"""

    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class InputRetrieveUpdateSerializer(serializers.ModelSerializer):
    """simple input RUD serializer"""

    class Meta:
        model = Input
        fields = base_fields


class InputCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = Input
        fields = base_element_fields


class SelectElementRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Select element RUD serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = SelectElement
        fields = base_fields + ['data', ]


class SelectElementCreateSerializer(serializers.ModelSerializer):
    """Select element create serializer"""
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = SelectElement
        fields = base_element_fields + ['data', ]


class DateTimeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = base_fields


# map of element types to their serializers
_serializers = {
    INPUT: {'retrieve': InputRetrieveUpdateSerializer},
    DATETIME: {'retrieve': DateTimeRetrieveSerializer},
    SELECT: {'retrieve': SelectElementRetrieveUpdateSerializer}
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
