from core.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Django user serializer"""

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'email', 'is_active',
                  'first_name', 'last_name', 'is_superuser', ]

        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Internal User Profile serializer"""

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['pk', 'user', 'token']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # create user profile
        user = User.objects.create_user(**user_data)

        # create user profile
        user_profile = UserProfile(**validated_data, user=user)
        user_profile.save()

        return user_profile
