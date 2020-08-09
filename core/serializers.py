from rest_framework import serializers

from core.models import Input, Data, DateTimeElement, SelectElement


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class InputRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ['pk', 'value']


class SelectElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectElement
        fields = ['pk', 'value', 'data']


class DateTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeElement
        fields = ['pk', 'value']
