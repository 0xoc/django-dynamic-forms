from rest_framework.permissions import BasePermission


class IsLoggedIn(BasePermission):
    """
    Check if user is authenticated and is active
    """
    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.is_active


class IsSuperuser(BasePermission):
    """Check if logged in user is a super user
    Authentication is not checked, You should check for IsLoggedIn first
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
