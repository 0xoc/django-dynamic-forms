from abc import ABC

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
    """
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=element_types, default=INPUT)

    # this field should be set according to the data type
    # Ex.: a simple text filed may be stored in CharField
    # Ex.: to store a datetime, value may be DateTimeField
    value = models.CharField(max_length=1024)

    # array of available filters on an element
    filters = ['icontains', 'startswith', 'endswith']

    def to_representation(self):
        """External representation of the value"""
        pass

    def to_internal_value(self, raw_value):
        """ convert external(raw) value to internal value """

    @property
    def data(self):
        return None


class Input(Element):
    """ Simple Text Input """
    pass
