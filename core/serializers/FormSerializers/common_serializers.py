from rest_framework import serializers

from core.models import Data


class DataSerializer(serializers.ModelSerializer):
    """Element Extra data CRUD serializer"""

    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']