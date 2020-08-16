from django.db import models, transaction
from rest_framework.authtoken.models import Token

from .element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE, TIME, INT, FLOAT
from django.contrib.auth.models import User

from .sub_form_fields import get_related_elements


class UserProfile(models.Model):
    """User profile"""
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    @property
    def token(self) -> str:
        token, created = Token.objects.get_or_create(user=self.user)
        return str(token.key)


class Form(models.Model):
    filler = models.ForeignKey(UserProfile, related_name="forms",
                               on_delete=models.SET_NULL, blank=True, null=True)
    creator = models.ForeignKey(UserProfile, related_name="templates",
                                on_delete=models.CASCADE)
    base_template = models.ForeignKey("Form", related_name="forms", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)

    def create_filling_form(self):
        with transaction.atomic():

            # duplicate form info
            if not self.base_template:
                _base_template = Form.objects.get(pk=self.pk)
            else:
                _base_template = self.base_template

            self.base_template = _base_template
            self.pk = None

            self.save()

            # duplicate sub_forms
            for sub_form in self.base_template.sub_forms.all():
                _fields = sub_form.fields.all()

                sub_form.pk = None
                sub_form.form = self
                sub_form.save()

                # duplicate sub form fields
                for field in _fields:
                    _elements = get_related_elements(field)

                    field.pk = None
                    field.sub_form = sub_form
                    field.save()

                    # duplicate elements
                    for element in _elements:
                        element.pk = None
                        element.field = field
                        element.save()
        return self

class SubForm(models.Model):
    """
    SubForms make up different sections of each form
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    order = models.IntegerField(default=0)
    form = models.ForeignKey(Form, related_name="sub_forms", on_delete=models.CASCADE)
    is_grid = models.BooleanField(default=False)


class Field(models.Model):
    """
    A field consists of one or more field elements
    """
    sub_form = models.ForeignKey(SubForm, related_name="fields", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)


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
    title = models.CharField(max_length=255)
    type = "ABC"

    # display order of the field
    order = models.IntegerField(default=0)

    field = models.ForeignKey(Field, related_name="elements_%(class)s", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Input(Element):
    """ Simple Text Input """
    value = models.CharField(max_length=1024, blank=True, null=True)
    type = INPUT
    filters = ['icontains', 'startswith', 'endswith']


class DateTimeElement(Element):
    """Date time field """

    value = models.DateTimeField(blank=True, null=True)
    type = DATETIME
    filters = ['', 'gt', 'lt', 'gte', 'lte']


class SelectElement(Element):
    """Html select element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    type = SELECT
    filters = ['', ]  # empty filter string means exact match

    data = models.ManyToManyField("Data")


class RadioElement(Element):
    """Html radio element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    type = RADIO
    filters = ['', ]  # empty filter string means exact match

    data = models.ManyToManyField("Data")


class CharField(models.Model):
    """Raw char field"""
    value = models.CharField(max_length=1024, blank=True, null=True)
    check_box = models.ForeignKey("CheckboxElement", related_name="values", on_delete=models.CASCADE)


class CheckboxElement(Element):
    """Html checkbox element with options"""

    type = CHECKBOX
    filters = ['', ]  # empty filter string means exact match

    data = models.ManyToManyField("Data")


class DateElement(Element):
    """Html date element with options"""

    value = models.DateField(blank=True, null=True)
    type = DATE
    filters = ['', 'gt', 'lt', 'gte', 'lte']  # empty filter string means exact match


class TimeElement(Element):
    """Html TimeField element with options"""

    value = models.TimeField(blank=True, null=True)
    type = TIME
    filters = ['', 'gt', 'lt', 'gte', 'lte']  # empty filter string means exact match


class IntegerField(Element):
    """Html Int element with options"""

    value = models.IntegerField(blank=True, null=True)
    type = INT
    filters = ['', 'gt', 'lt', 'gte', 'lte']  # empty filter string means exact match


class FloatField(Element):
    """Html TimeField element with options"""

    value = models.FloatField(blank=True, null=True)
    type = FLOAT
    filters = ['', 'gt', 'lt', 'gte', 'lte']  # empty filter string means exact match


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
    INT: IntegerField
}
