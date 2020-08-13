from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsSuperuser, IsLoggedIn
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer


class CreateUserProfileView(CreateAPIView):
    """Create User Profile
    registration is closed, only existing admins can add new users
    """
    permission_classes = [IsLoggedIn, IsSuperuser]

    serializer_class = UserProfileCreateSerializer
