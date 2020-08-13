from core.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Django user serializer"""

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'email',
                  'first_name', 'last_name', 'is_superuser', 'is_staff']

        extra_kwargs = {
            'password': {'write-only': True}
        }


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Internal User Profile serializer"""

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['pk', 'user']

