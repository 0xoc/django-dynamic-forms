from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsSuperuser, IsLoggedIn
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer


class CreateUserProfileView(CreateAPIView):
    """Create User Profile
    registration is closed, only existing admins can add new users
    """
    permission_classes = [IsLoggedIn, IsSuperuser]

    serializer_class = UserProfileCreateSerializer


class MyUserProfileInfo(RetrieveUpdateDestroyAPIView):
    """RUD currently logged in user"""
    permission_classes = [IsLoggedIn, ]
    serializer_class = UserProfileCreateSerializer

    def get_object(self):
        return self.request.user.user_profile


class UserProfileInfo(RetrieveUpdateDestroyAPIView):
    """RUD any user"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = UserProfileCreateSerializer

    lookup_url_kwarg = 'user_profile_id'
    lookup_field = 'pk'
