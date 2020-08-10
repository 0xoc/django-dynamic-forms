from rest_framework import serializers

from core.models import Input, SelectElement, SubForm, Element, DateTimeElement
from core.serializers.common_serializers import DataSerializer
from core.element_types import INPUT, DATETIME, SELECT
from core.element_types import element_types
from core.serializers.serializers_headers import abstract_element_fields, base_element_fields


class ElementCreteSerializer(serializers.ModelSerializer):
    """Abstract element serializer"""

    class Meta:
        model = Element
        fields = abstract_element_fields
        abstract = True


class InputCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = Input
        fields = base_element_fields


class SelectElementCreateSerializer(serializers.ModelSerializer):
    """Select element create serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = SelectElement
        fields = base_element_fields + ['data', ]


class DataTimeCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = DateTimeElement
        fields = base_element_fields


# map of element types to their create serializer
create_serializers = {
    INPUT: InputCreateSerializer,
    DATETIME: DataTimeCreateSerializer,
    SELECT: SelectElementCreateSerializer
}


class SubFormRawCreateSerializer(serializers.ModelSerializer):
    """Create a raw sub form,
    a raw sub form is a sub from without any fields,
     only meta data"""

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description']
