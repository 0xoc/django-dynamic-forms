from django.db import transaction
from rest_framework import serializers

from core.models import Input, SelectElement, SubForm, DateTimeElement, Data, Field, RadioElement, \
    CheckboxElement, DateElement, TimeElement, Template, IntegerField, FloatField, CharField, TextArea, \
    Form, elements
from core.serializers.FormSerializers.common_serializers import DataSerializer, CharFieldSerializer
from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT, TEXTAREA, BOOLEAN
from core.serializers.FormSerializers.serializers_headers import abstract_element_fields
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfilePublicRetrieve


def get_raw_converter_serializer(element_type):
    """converts raw json value to native python types value"""

    class _Serializer(serializers.ModelSerializer):
        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            fields = ['pk', model.value_field]

    return _Serializer


class CreateElementWithData(serializers.ModelSerializer):
    """Base create serializer with extra data support"""

    data = DataSerializer(many=True, required=False)

    class Meta:
        model = None

    def create(self, validated_data):
        _Model = self.Meta.model

        data_data = validated_data.pop('data', [])

        data_objects = [Data(**data_data_) for data_data_ in data_data]

        for data_object in data_objects:
            data_object.save()

        _model = _Model(**validated_data)
        _model.save()

        _model.data.add(*data_objects)

        return _model


def get_create_serializer(element_type):
    """Get element create serializer based on element type"""

    class _CreateSerializer(CreateElementWithData):

        # use char field serializer if multiple values are possible for the given element
        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            fields = abstract_element_fields + [model.value_field, ]

        def create(self, validated_data):
            # if element has multiple values (value filed is "values")
            # create values objects

            if elements.get(element_type).value_field == "values":
                values = validated_data.pop('values', None)
                obj = super(_CreateSerializer, self).create(validated_data)

                # create values
                for value in values:
                    _value = CharField.objects.create(**value)
                    obj.values.add(_value)

                return obj
            else:
                # object is single valued
                return super(_CreateSerializer, self).create(validated_data)

    return _CreateSerializer


def get_update_serializer(element_type):
    class UpdateSerializer(serializers.ModelSerializer):
        data = DataSerializer(many=True)

        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            fields = abstract_element_fields + [model.value_field, 'data', ]

        def update(self, instance, validated_data):
            _data = validated_data.pop('data', [])
            _values = validated_data.pop('values', [])

            with transaction.atomic():
                # delete all data
                for __data in instance.data.all():
                    __data.delete()

                # add new data
                for __data in _data:
                    ___data = Data.objects.create(**__data)
                    instance.data.add(___data)

                if self.Meta.model.value_field == "values":
                    # delete all values
                    for _value in instance.values.all():
                        _value.delete()

                    # add values
                    for _value in _values:
                        __value = CharField.objects.create(**_value)
                        instance.values.add(__value)

            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance.refresh_from_db()

            return instance

    return UpdateSerializer


def get_set_value_serializer(element_type):
    """Return set value serializer, set value serializer provides
    a serializer that either
    updates the value field or values field based on element type"""

    class SetValueSerializer(serializers.ModelSerializer):
        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            fields = ['pk', model.value_field, ]

        def update(self, instance, validated_data):
            values = validated_data.pop('values', [])

            if self.Meta.model.value_field == 'values':
                # remove old values and set new values

                for value in instance.values.all():
                    value.delete()

                # add new values
                for value in values:
                    _value = CharField(**value)
                    _value.save()

                    instance.values.add(_value)

                return instance
            else:
                instance.value = validated_data.get('value')
                instance.save()
                return instance

    return SetValueSerializer


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


class FormCreateSerializer(serializers.ModelSerializer):
    """Create from from base template"""
    filler = UserProfilePublicRetrieve(read_only=True)

    class Meta:
        model = Form
        fields = ['pk', 'filler', 'template', 'fork_date', 'last_change_date', 'description']
