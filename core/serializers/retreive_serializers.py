from rest_framework import serializers

from core.element_types import INPUT, DATETIME, SELECT
from core.models import Input, SelectElement, DateTimeElement, SubForm
from core.serializers.common_serializers import DataSerializer
from core.serializers.serializers_headers import base_fields
from core.sub_form_fields import get_related_fields


class InputRetrieveUpdateSerializer(serializers.ModelSerializer):
    """simple input RUD serializer"""

    class Meta:
        model = Input
        fields = base_fields


class SelectElementRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Select element RUD serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = SelectElement
        fields = base_fields + ['data', ]


class DateTimeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = base_fields


# map of element types to their retrieve serializer
retrieve_serializers = {
    INPUT: InputRetrieveUpdateSerializer,
    DATETIME: DateTimeRetrieveSerializer,
    SELECT: SelectElementRetrieveUpdateSerializer
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
            _Serializer = retrieve_serializers.get(type(field).type)
            _field_data = _Serializer(instance=field).data
            _fields_data.append(_field_data)

        return _fields_data
