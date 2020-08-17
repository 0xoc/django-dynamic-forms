from rest_framework import serializers

from core.models import Input, SelectElement, SubForm, DateTimeElement, Data, Field, RadioElement, \
    CheckboxElement, DateElement, TimeElement, Template, IntegerField, FloatField, CharField, TextArea, BooleanField
from core.serializers.FormSerializers.common_serializers import DataSerializer, CharFieldSerializer
from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT, TEXTAREA, BOOLEAN
from core.serializers.FormSerializers.serializers_headers import base_element_fields, abstract_element_fields


class InputCreateSerializer(serializers.ModelSerializer):
    """simple input create serializer"""

    class Meta:
        model = Input
        fields = base_element_fields


class BooleanCreateSerializer(serializers.ModelSerializer):
    """boolean create serializer"""

    class Meta:
        model = BooleanField
        fields = base_element_fields


class TextAreaCreateSerializer(serializers.ModelSerializer):
    """text area create serializer"""

    class Meta:
        model = TextArea
        fields = base_element_fields


class IntegerCreateSerializer(serializers.ModelSerializer):
    """int create serializer"""

    class Meta:
        model = IntegerField
        fields = base_element_fields


class FloatCreateSerializer(serializers.ModelSerializer):
    """float create serializer"""

    class Meta:
        model = FloatField
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
    values = CharFieldSerializer(many=True)

    class Meta:
        model = CheckboxElement
        fields = abstract_element_fields + ['data', 'values']

    def create(self, validated_data):
        values = validated_data.pop('values', None)
        check_box = super(CheckboxCreateSerializer, self).create(validated_data)

        # create values
        for value in values:
            CharField.objects.create(**value, check_box=check_box)

        return check_box


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
    INT: IntegerCreateSerializer,
    FLOAT: FloatCreateSerializer,
    TEXTAREA: TextAreaCreateSerializer,
    BOOLEAN: BooleanCreateSerializer
}


class TemplateRawCreateSerializer(serializers.ModelSerializer):
    """Create raw form as a template"""

    class Meta:
        model = Template
        fields = ['pk', 'title']


class SubFormRawCreateSerializer(serializers.ModelSerializer):
    """Create a raw sub form,
    a raw sub form is a sub from without any fields,
     only meta data"""

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'template', ]


class FieldRawCreateSerializer(serializers.ModelSerializer):
    """
    Create raw field, a raw field has a title and a form id
    other filed elements
    """

    class Meta:
        model = Field
        fields = ['pk', 'title', 'sub_form', 'order', 'is_grid']
