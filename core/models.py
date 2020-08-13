from django.db import models
from rest_framework.authtoken.models import Token

from .element_types import INPUT, DATETIME, SELECT, RADIO, CHECKBOX, DATE
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User profile"""
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    @property
    def token(self) -> str:
        token, created = Token.objects.get_or_create(user=self.user)
        return str(token.key)


class Form(models.Model):
    """ Form """
    pass


class SubForm(models.Model):
    """
    SubForms make up different sections of each form
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    order = models.IntegerField(default=0)


class Field(models.Model):
    """
    A field consists of one or more field elements
    """
    sub_form = models.ForeignKey(SubForm, related_name="fields", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)


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
    filters = ['gt', 'lt']


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


class CheckboxElement(Element):
    """Html checkbox element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    type = CHECKBOX
    filters = ['', ]  # empty filter string means exact match

    data = models.ManyToManyField("Data")


class DateElement(Element):
    """Html date element with options"""

    value = models.DateField(blank=True, null=True)
    type = DATE
    filters = ['', ]  # empty filter string means exact match


class TimeElement(Element):
    """Html TimeField element with options"""

    value = models.TimeField(blank=True, null=True)
    type = DATE
    filters = ['', ]  # empty filter string means exact match


class Data(models.Model):
    """ Extra data used on select, radio, checkbox elements"""
    value = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
