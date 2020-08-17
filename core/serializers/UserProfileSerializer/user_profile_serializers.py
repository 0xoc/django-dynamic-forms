from abc import ABC

from core.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    """Django user serializer"""

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'email', 'is_active',
                  'first_name', 'last_name', 'is_superuser', ]

        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Django user serializer"""

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'is_active',
                  'first_name', 'last_name', 'is_superuser', ]


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Internal User Profile serializer"""

    user = UserCreateSerializer()

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

    def update(self, instance, validated_data):
        # ignore password
        validated_data.pop('password', None)

        user_updates = validated_data.pop('user')

        # update user
        User.objects.filter(pk=instance.user.pk).update(**user_updates)

        # update user
        UserProfile.objects.filter(pk=instance.pk).update(**validated_data)

        instance.refresh_from_db()

        return instance


class UserProfilePublicRetrieve(serializers.ModelSerializer):
    """Profile serializer"""

    user = UserRetrieveSerializer()

    class Meta:
        model = UserProfile
        fields = ['pk', 'user', ]


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()