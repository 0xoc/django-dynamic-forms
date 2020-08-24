from django.db import models, transaction
from rest_framework.authtoken.models import Token

from .element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT, TEXTAREA, BOOLEAN
from django.contrib.auth.models import User

from .sub_form_fields import get_related_attrs


class UserProfile(models.Model):
    """User profile"""
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    @property
    def token(self) -> str:
        token, created = Token.objects.get_or_create(user=self.user)
        return str(token.key)

    def __str__(self):
        return str(self.user)


class Template(models.Model):
    """Base template for a form that can be filled later"""
    creator = models.ForeignKey(UserProfile, related_name="templates",
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    @property
    def forms_count(self):
        return self.forms.count()

    def __str__(self):
        return str(self.title)


class Form(models.Model):
    """A Form is like a fork of a template, it includes elements,
    but elements are regarded as answers to the base template"""

    filler = models.ForeignKey(UserProfile, related_name="filled_forms", on_delete=models.CASCADE)
    fork_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)
    template = models.ForeignKey(Template, related_name="forms", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default="")

    def __str__(self):
        return "%s - %s" % (str(self.template), str(self.description))


class SubForm(models.Model):
    """
    SubForms make up different sections of each form
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    order = models.IntegerField(default=0)
    template = models.ForeignKey(Template, related_name="sub_forms", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (str(self.template), str(self.title))


class Field(models.Model):
    """
    A field consists of one or more field elements
    """
    sub_form = models.ForeignKey(SubForm, related_name="fields", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_grid = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (str(self.sub_form), str(self.title))


class Element(models.Model):
    """
    Base class for an input element (defaults to simple text field)
    value and filters fields may be overridden
    to cope with other input types

    # this field should be set according to the data type
    # Ex.: a simple text filed may be stored in CharField
    # Ex.: to store a datetime, value may be DateTimeField
    value = models.CharField(max_length=1024, blank=True, null=True)

    # array of available filters on an elements
    filters = ['icontains', 'startswith', 'endswith']

    all sub classes of element will be related to a sub form with a related named of the
    following format: fields_class_name, where class_name is the name of the subclass :)

    """

    # if the given element is used as answer
    # title, type, order, and field will be inherited from the question field
    # when serializing the element
    title = models.CharField(max_length=255)

    # Ex.: Input, checkbox, datetime, ...
    type = "ABC"

    # some element may have more than one value at a given time (Ex. Check box)
    # these elements save their values in "values" field as a CharField model
    # default value field for elements is "value"
    value_field = 'value'

    # any extra data that may be needed for the given element, can be saved in Data as
    # display, value pairs
    data = models.ManyToManyField("Data", blank=True)

    # display order of the field
    order = models.IntegerField(default=0)
    field = models.ForeignKey(Field, related_name="elements_%(class)s",
                              on_delete=models.CASCADE, blank=True, null=True)

    # these fields are used for an element that
    # will be regarded as an answer to an element of the same type
    answer_of = models.ForeignKey("self", related_name="answers",
                                  on_delete=models.CASCADE, blank=True, null=True)
    form = models.ForeignKey(Form, related_name="answers_%(class)s",
                             on_delete=models.CASCADE, blank=True, null=True)

    quantitative_filters = [{"value": '', "display": "مساوی"},
                           {"value": 'gt', "display": "بزرگتر"},
                           {"value": 'lt', "display": "کوچکتر"},
                           {"value": 'gte', "display": "بزرگتر مساوی"},
                           {"value": 'lte', "display": "کوچکتر مساوی"}
                           ]
    literal_filters = [
        {"value": "", "display": "مساوی"},
        {"value": 'icontains ', "display": "دربر دارد"},
        {"value": 'startswith', "display": "شروع میشود با"},
        {"value": 'endswith', "display": "پایان میابد با"}
    ]

    @classmethod
    def related_name_to_form(cls):
        return "answers_%s" % str.lower(cls.__name__)

    @property
    def display_title(self):
        return "%s -> %s -> %s" % (self.field.sub_form.title if self.field.sub_form.title else "", 
        self.field.title if self.field.title else " ", self.title if self.title else "")

    def __str__(self):
        return "%s - %s" % (str(self.field), str(self.title))

    class Meta:
        unique_together = ['answer_of', 'form']
        abstract = True


class Input(Element):
    """ Simple Text Input """
    value = models.CharField(max_length=1024, blank=True, null=True)
    type = INPUT
    filters = Element.literal_filters


class TextArea(Element):
    """ Simple Text Input """
    value = models.CharField(max_length=10240, blank=True, null=True)
    type = TEXTAREA
    filters = Element.literal_filters


class DateTimeElement(Element):
    """Date time field """

    value = models.DateTimeField(blank=True, null=True)
    type = DATETIME
    filters = Element.quantitative_filters


class SelectElement(Element):
    """Html select element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    type = SELECT
    filters = [{"value": '', "display": 'مساوی'}, ]  # empty filter string means exact match


class RadioElement(Element):
    """Html radio element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    type = RADIO
    filters = [{"value": '', "display": 'مساوی'}, ]  # empty filter string means exact match


class CharField(models.Model):
    """Raw char field"""
    value = models.CharField(max_length=1024, blank=True, null=True)


class CheckboxElement(Element):
    """Html checkbox element with options"""

    values = models.ManyToManyField(CharField, blank=True)
    type = CHECKBOX
    filters = [{"value": 'value__contains', "display": 'شامل'}, ]  # empty filter string means exact match
    value_field = 'values'


class DateElement(Element):
    """Html date element with options"""

    value = models.DateField(blank=True, null=True)
    type = DATE
    filters = Element.quantitative_filters


class TimeElement(Element):
    """Html TimeField element with options"""

    value = models.TimeField(blank=True, null=True)
    type = TIME
    filters = Element.quantitative_filters


class IntegerField(Element):
    """Html Int element with options"""

    value = models.IntegerField(blank=True, null=True)
    type = INT
    filters = Element.quantitative_filters


class FloatField(Element):
    """Html TimeField element with options"""

    value = models.FloatField(blank=True, null=True)
    type = FLOAT
    filters = Element.quantitative_filters


class Data(models.Model):
    """ Extra data used on select, radio, checkbox elements"""
    value = models.CharField(max_length=255)
    display = models.CharField(max_length=255)


elements = {
    INPUT: Input,
    DATE: DateElement,
    TIME: TimeElement,
    DATETIME: DateTimeElement,
    RADIO: RadioElement,
    CHECKBOX: CheckboxElement,
    SELECT: SelectElement,
    INT: IntegerField,
    TEXTAREA: TextArea,
    FLOAT: FloatField
}
