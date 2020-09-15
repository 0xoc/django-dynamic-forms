from rest_framework import serializers

from core.element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT, TEXTAREA, BOOLEAN
from core.models import Input, SelectElement, DateTimeElement, SubForm, Field, CheckboxElement, DateElement, \
    TimeElement, Template, IntegerField, FloatField, TextArea, elements, Form
from core.serializers.FormSerializers.common_serializers import DataSerializer, CharFieldSerializer
from core.serializers.FormSerializers.serializers_headers import base_fields, base_field_fields, abstract_base_fields, \
    abstract_element_fields, base_field_fields_simple
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer, \
    UserProfilePublicRetrieve
from core.sub_form_fields import get_related_attrs


def get_retrieve_serializer(element_type, simple=False):
    """Return retrieve serializer base od element type"""

    class _RetrieveSerializer(serializers.ModelSerializer):
        data = DataSerializer(many=True)

        if not simple:
            filters = serializers.SerializerMethodField()

        if elements.get(element_type).value_field == "values":
            values = CharFieldSerializer(many=True)

        class Meta:
            model = elements.get(element_type)
            if not simple:
                fields = abstract_element_fields + [elements.get(element_type).value_field, 'filters', 'display_title',
                                                    'uid', 'display_title_full']
            else:
                fields = abstract_element_fields + [elements.get(element_type).value_field, 'uid', ]

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
        _elements = get_related_attrs(instance)
        _elements_data = []

        for _element in _elements:
            _Serializer = get_retrieve_serializer(type(_element).type)
            _field_data = _Serializer(instance=_element).data
            _elements_data.append(_field_data)

        return _elements_data


class FieldAnswerRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve a field with it's elements"""
    elements = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = base_field_fields

    def get_elements(self, instance):

        _elements = get_related_attrs(instance)
        _elements_data = []

        for _element in _elements:
            _Serializer = get_retrieve_serializer(type(_element).type)
            _element_data = _Serializer(instance=_element).data

            if _element.answer_of is None:
                # this field is not an answer
                # fined it's answer

                try:
                    AnswerModel = elements.get(_element.type)
                    _obj = AnswerModel.objects.get(answer_of=_element, form=self.context.get('form'))
                    _new_data = _Serializer(instance=_obj).data

                    _elements_data[type(_element).value_field] = _new_data[type(_element).value_field]

                except AnswerModel.DoesNotExist:
                    pass
            else:
                continue

            _elements_data.append(_element_data)

        return _elements_data


class SubFormAnswerRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve Sub Form data with is's inputs and input elements"""
    fields = serializers.SerializerMethodField('get_fields_data')

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'order', 'template', 'fields']

    def get_fields_data(self, instance):
        _serializer = FieldAnswerRetrieveSerializer(instance=instance.fields.all().order_by('order'),
                                                    many=True,
                                                    context={"form": self.context.get('form')})
        return _serializer.data


class FieldSimpleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = base_field_fields_simple


class SubFormRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve Sub Form data with is's inputs and input elements"""
    fields = FieldRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'fields', 'order', 'template']


class SubFormSimpleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubForm
        fields = ['pk', 'title', 'description', 'order', 'order', 'template']


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
    sub_forms = serializers.SerializerMethodField()

    filler = UserProfilePublicRetrieve(read_only=True)
    template = TemplateSimpleRetrieveSerializer(read_only=True)

    class Meta:
        model = Form
        fields = ['pk', 'filler', 'fork_date', "sub_forms", 'template', 'description']

    @staticmethod
    def get_sub_forms(instance):
        _serializers = SubFormAnswerRetrieveSerializer(instance=instance.template.sub_forms.all().order_by('order'),
                                                       many=True,
                                                       context={"form": instance})
        return _serializers.data
    # @staticmethod
    # def get_sub_forms(instance):
    #     sub_forms_data = []
    #
    #     template = instance.template
    #     sub_forms = template.sub_forms.all().order_by('order')
    #     # print("subform ordering done")
    #     print("start------------------>")
    #     for sub_form in sub_forms:
    #         data = SubFormRetrieveSerializer(instance=sub_form).data
    #         print("subform serialization done")
    #         # over ride this
    #         # data['fields']
    #         data['fields'] = []
    #
    #         for field in sub_form.fields.all().order_by('order'):
    #             # print("field ordering done")
    #             base_field_data = FieldSimpleRetrieveSerializer(instance=field).data
    #
    #             # print("field serialization done")
    #             base_field_data['elements'] = []
    #
    #             for element in get_related_attrs(field):
    #                 if element.answer_of is not None:
    #                     continue
    #                 AnswerModel = elements.get(element.type)
    #                 _serializer = get_retrieve_serializer(AnswerModel.type, simple=True)
    #                 base_element_data = _serializer(instance=element).data
    #
    #                 try:
    #                     # if the element has an answer(it itself is not a raw template element)
    #                     # find the answer and serialize it
    #                     answer = AnswerModel.objects.get(answer_of=element, form=instance)
    #                     answer_data = _serializer(instance=answer).data
    #                     base_element_data[AnswerModel.value_field] = answer_data[AnswerModel.value_field]
    #
    #                     base_field_data['elements'].append(base_element_data)
    #
    #                 except AnswerModel.DoesNotExist:
    #                     base_field_data['elements'].append(base_element_data)
    #
    #             data['fields'].append(base_field_data)
    #         sub_forms_data.append(data)
    #
    #     print("<------------------end")
    #     return sub_forms_data


class FormSimpleRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve form info with filler info and detailed sub_form info"""
    filler = UserProfilePublicRetrieve(read_only=True)
    template = TemplateSimpleRetrieveSerializer(read_only=True)

    class Meta:
        model = Form
        fields = ['pk', 'filler', 'fork_date', 'last_change_date', 'template',
                  'template', 'description']


class FormFilterSerializer(serializers.Serializer):
    query = serializers.JSONField(write_only=True, required=True)
    elements = serializers.JSONField(write_only=True, required=True)

    @staticmethod
    def validate_query(query):
        if not query:
            serializers.ValidationError("Empty filter query")
        return query

    @staticmethod
    def validate_elements(element):
        if not element:
            serializers.ValidationError("Empty elements query")
        return element
