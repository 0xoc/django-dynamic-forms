from rest_framework import serializers

from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT
from core.models import Input, SelectElement, DateTimeElement, SubForm, Field, CheckboxElement, DateElement, \
    TimeElement, Form, IntegerField, FloatField
from core.serializers.FormSerializers.common_serializers import DataSerializer, CharFieldSerializer
from core.serializers.FormSerializers.serializers_headers import base_fields, base_field_fields, abstract_base_fields
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer, \
    UserProfilePublicRetrieve
from core.sub_form_fields import get_related_elements


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


class RadioRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Radio RUD serializer"""
    data = DataSerializer(many=True)

    class Meta:
        model = SelectElement
        fields = base_fields + ['data', ]


class CheckboxRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Checkbox RUD serializer"""
    data = DataSerializer(many=True)
    values = CharFieldSerializer(many=True)

    class Meta:
        model = CheckboxElement
        fields = abstract_base_fields + ['data', 'values']


class DateRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Checkbox RUD serializer"""

    class Meta:
        model = DateElement
        fields = base_fields


class TimeRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Checkbox RUD serializer"""

    class Meta:
        model = TimeElement
        fields = base_fields


class IntegerRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Integer RUD serializer"""

    class Meta:
        model = IntegerField
        fields = base_fields


class FloatRetrieveUpdateSerializer(serializers.ModelSerializer):
    """Float RUD serializer"""

    class Meta:
        model = FloatField
        fields = base_fields


class DateTimeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = base_fields


# map of element types to their retrieve serializer
retrieve_serializers = {
    INPUT: InputRetrieveUpdateSerializer,
    DATETIME: DateTimeRetrieveSerializer,
    SELECT: SelectElementRetrieveUpdateSerializer,
    RADIO: RadioRetrieveUpdateSerializer,
    CHECKBOX: CheckboxRetrieveUpdateSerializer,
    DATE: DateRetrieveUpdateSerializer,
    TIME: TimeRetrieveUpdateSerializer,
    INT: IntegerRetrieveUpdateSerializer,
    FLOAT: FloatRetrieveUpdateSerializer
}


class FieldRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve a field with it's elements"""
    elements = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = base_field_fields

    @staticmethod
    def get_elements(instance):
        _fields = get_related_elements(instance)
        _fields_data = []

        for field in _fields:
            _Serializer = retrieve_serializers.get(type(field).type)
            _field_data = _Serializer(instance=field).data
            _fields_data.append(_field_data)

        return _fields_data


class SubFormRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve Sub Form data with is's inputs and input elements"""
    fields = FieldRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'fields', 'order', 'is_grid']


class FormRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    sub_forms = SubFormRetrieveSerializer(many=True, read_only=True)
    filler = UserProfilePublicRetrieve()

    class Meta:
        model = Form
        fields = ['pk', "filler", 'base_template', "sub_forms"]
