from abc import ABC

from django.db import models
from .element_types import element_types, INPUT
from django.utils.dateparse import parse_datetime


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
    """
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=element_types, default=INPUT)

    # this field should be set according to the data type
    # Ex.: a simple text filed may be stored in CharField
    # Ex.: to store a datetime, value may be DateTimeField
    # value = models.CharField(max_length=1024, blank=True, null=True)

    # array of available filters on an element
    # filters = ['icontains', 'startswith', 'endswith']


class Input(Element):
    """ Simple Text Input """
    value = models.CharField(max_length=1024, blank=True, null=True)
    filters = ['icontains', 'startswith', 'endswith']

    sub_form = models.ForeignKey(SubForm, related_name="inputs", on_delete=models.CASCADE)


class DateTimeElement(Element):
    """Date time field """

    value = models.DateTimeField(blank=True, null=True)
    filters = ['gt', 'lt']

    sub_form = models.ForeignKey(SubForm, related_name="date_times", on_delete=models.CASCADE)


class SelectElement(Element, models.Model):
    """Html select element with options """

    value = models.CharField(max_length=1024, blank=True, null=True)
    filters = ['', ]  # empty filter string means exact match

    sub_form = models.ForeignKey(SubForm, related_name="selects", on_delete=models.CASCADE)


class Option(models.Model):
    """ An option in the select element """
    value = models.CharField(max_length=255)
    display = models.CharField(max_length=255)

    select_form = models.ForeignKey("SelectElement", related_name="options", on_delete=models.CASCADE)
