from rest_framework import serializers

from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT, TEXTAREA, BOOLEAN
from core.models import Input, SelectElement, DateTimeElement, SubForm, Field, CheckboxElement, DateElement, \
    TimeElement, Template, IntegerField, FloatField, TextArea, elements, Form
from core.serializers.FormSerializers.common_serializers import DataSerializer, CharFieldSerializer
from core.serializers.FormSerializers.serializers_headers import base_fields, base_field_fields, abstract_base_fields, \
    abstract_element_fields
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer, \
    UserProfilePublicRetrieve
from core.sub_form_fields import get_related_attrs


def get_retrieve_serializer(element_type):
    """Return retrieve serializer base od element type"""

    class _RetrieveSerializer(serializers.ModelSerializer):
        data = DataSerializer(many=True)
        filters = serializers.SerializerMethodField()

        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            fields = abstract_element_fields + [elements.get(element_type).value_field, 'filters', 'display_title', 'uid']

        @staticmethod
        def get_filters(instance):
            return instance.filters

    return _RetrieveSerializer


class FieldRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve a field with it's elements"""
    elements = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = base_field_fields

    @staticmethod
    def get_elements(instance):
        _fields = get_related_attrs(instance)
        _fields_data = []

        for field in _fields:
            _Serializer = get_retrieve_serializer(type(field).type)
            _field_data = _Serializer(instance=field).data
            _fields_data.append(_field_data)

        return _fields_data


class SubFormRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve Sub Form data with is's inputs and input elements"""
    fields = FieldRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'fields', 'order', 'template']


class TemplateRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    sub_forms = SubFormRetrieveSerializer(many=True, read_only=True)
    creator = UserProfilePublicRetrieve(read_only=True)

    class Meta:
        model = Template
        fields = ['pk', 'creator', "sub_forms", "title", 'forms_count', 'access_level']


class TemplateSimpleRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    creator = UserProfilePublicRetrieve()

    class Meta:
        model = Template
        fields = ['pk', 'creator', "title", 'forms_count', 'access_level']

class FormRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    sub_forms = serializers.SerializerMethodField(read_only=True)
    filler = UserProfilePublicRetrieve(read_only=True)

    class Meta:
        model = Form
        fields = ['pk', 'filler', 'fork_date', 'last_change_date', "sub_forms", 'template', 'description']

    @staticmethod
    def get_sub_forms(instance):
        sub_forms_data = []

        template = instance.template
        sub_forms = template.sub_forms.all().order_by('order')

        for sub_form in sub_forms:
            data = SubFormRetrieveSerializer(instance=sub_form).data
            # over ride this
            # data['fields']
            data['fields'] = []

            for field in sub_form.fields.all().order_by('order'):
                base_field_data = FieldRetrieveSerializer(instance=field).data
                base_field_data['elements'] = []

                for element in get_related_attrs(field):
                    if element.answer_of is not None:
                        continue
                    AnswerModel = elements.get(element.type)
                    _serializer = get_retrieve_serializer(AnswerModel.type)
                    base_element_data = _serializer(instance=element).data

                    try:
                        answer = AnswerModel.objects.get(answer_of=element, form=instance)
                        answer_data = _serializer(instance=answer).data
                        base_element_data[AnswerModel.value_field] = answer_data[AnswerModel.value_field]

                        base_field_data['elements'].append(base_element_data)

                    except AnswerModel.DoesNotExist:
                        base_field_data['elements'].append(base_element_data)

                data['fields'].append(base_field_data)
            sub_forms_data.append(data)
        return sub_forms_data


class FormSimpleRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    filler = UserProfilePublicRetrieve(read_only=True)
    template = TemplateSimpleRetrieveSerializer(read_only=True)

    class Meta:
        model = Form
        fields = ['pk', 'filler', 'fork_date', 'last_change_date',  'template',
                  'template', 'description']


class FormFilterSerializer(serializers.Serializer):

    query = serializers.JSONField(write_only=True)

