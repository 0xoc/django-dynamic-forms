from rest_framework import serializers

from core.models import Data, CharField


class DataSerializer(serializers.ModelSerializer):
    """Element Extra data CRUD serializer"""

    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class CharFieldSerializer(serializers.ModelSerializer):
    """Create Char field"""

    class Meta:
        model = CharField
        fields = ['pk', 'value', ]