from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import UserProfile
from core.permissions import IsSuperuser, IsLoggedIn
from core.serializers.UserProfileSerializer.user_profile_serializers import UserProfileCreateSerializer, \
    AuthTokenSerializer


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
    queryset = UserProfile.objects.all()

    lookup_url_kwarg = 'user_profile_id'
    lookup_field = 'pk'


class UserProfileList(ListAPIView):
    """List of all users"""
    permission_classes = [IsLoggedIn, IsSuperuser]

    serializer_class = UserProfileCreateSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(~Q(user=self.request.user)).order_by('-id')


class AuthToken(GenericAPIView):
    """Return user with token"""
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_profile = UserProfile.objects.get(user__username=username)

            if user_profile.user.check_password(password):

                return Response(UserProfileCreateSerializer(instance=user_profile).data)

            raise UserProfile.DoesNotExist

        except UserProfile.DoesNotExist:
            return Response({'detail': "Invalid Username and password"}, status=400)
