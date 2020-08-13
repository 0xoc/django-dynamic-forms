from rest_framework import serializers

from core.models import Input, SelectElement, SubForm, DateTimeElement, Data, Field, RadioElement, \
    CheckboxElement, DateElement, TimeElement, Form
from core.serializers.FormSerializers.common_serializers import DataSerializer
from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME
from core.serializers.FormSerializers.serializers_headers import base_element_fields


class InputCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = Input
        fields = base_element_fields


class CreateElementWithData(serializers.ModelSerializer):
    class Meta:
        model = None

    def create(self, validated_data):
        _Model = self.Meta.model

        data_data = validated_data.pop('data')

        data_objects = [Data(**data_data_) for data_data_ in data_data]

        for data_object in data_objects:
            data_object.save()

        _model = _Model(**validated_data)
        _model.save()

        _model.data.add(*data_objects)

        return _model


class SelectElementCreateSerializer(CreateElementWithData):
    """Select element create serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = SelectElement
        fields = base_element_fields + ['data', ]


class RadioCreateSerializer(CreateElementWithData):
    """Radio create serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = RadioElement
        fields = base_element_fields + ['data', ]


class CheckboxCreateSerializer(CreateElementWithData):
    """Checkbox create serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = CheckboxElement
        fields = base_element_fields + ['data', ]


class DateCreateSerializer(serializers.ModelSerializer):
    """Date create serializer"""

    class Meta:
        model = DateElement
        fields = base_element_fields


class TimeCreateSerializer(serializers.ModelSerializer):
    """time create serializer"""

    class Meta:
        model = TimeElement
        fields = base_element_fields


class DataTimeCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = DateTimeElement
        fields = base_element_fields


# map of element types to their create serializer
create_serializers = {
    INPUT: InputCreateSerializer,
    DATETIME: DataTimeCreateSerializer,
    SELECT: SelectElementCreateSerializer,
    RADIO: RadioCreateSerializer,
    CHECKBOX: CheckboxCreateSerializer,
    DATE: DateCreateSerializer,
    TIME: TimeCreateSerializer,
}


class TemplateRawCreateSerializer(serializers.ModelSerializer):
    """Create raw form as a template"""

    class Meta:
        model = Form
        fields = ['pk', 'title']


class SubFormRawCreateSerializer(serializers.ModelSerializer):
    """Create a raw sub form,
    a raw sub form is a sub from without any fields,
     only meta data"""

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'form']


class FieldRawCreateSerializer(serializers.ModelSerializer):
    """
    Create raw field, a raw field has a title and a form id
    other filed elements
    """

    class Meta:
        model = Field
        fields = ['pk', 'title', 'sub_form', 'order']
