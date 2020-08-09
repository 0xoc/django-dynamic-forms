from django.db import models
from .element_types import element_types, INPUT


class Form(models.Model):
    """ Form """
    pass


class SubForm(models.Model):
    """
    SubForms make up different sections of each form
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)


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
    type = models.CharField(max_length=3, choices=element_types, default=INPUT)

    sub_form = models.ForeignKey(SubForm, related_name="fields_%(class)s", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Input(Element):
    """ Simple Text Input """
    value = models.CharField(max_length=1024, blank=True, null=True)
    filters = ['icontains', 'startswith', 'endswith']


class DateTimeElement(Element):
    """Date time field """

    value = models.DateTimeField(blank=True, null=True)
    filters = ['gt', 'lt']


class SelectElement(Element):
    """Html select element with options"""

    value = models.CharField(max_length=1024, blank=True, null=True)
    filters = ['', ]  # empty filter string means exact match

    data = models.ManyToManyField("Data")


class Data(models.Model):
    """ Extra data used on select, radio, checkbox elements"""
    value = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
