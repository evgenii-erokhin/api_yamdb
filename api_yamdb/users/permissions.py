from rest_framework.permissions import (BasePermission, IsAdminUser,
                                        IsAuthenticated)

from .models import User


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        user = User.objects.get(id=request.user.id)
        return bool(request.user and (user.role == 'admin'
                                      or user.is_superuser))


class IsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.id:
            return True
        return False


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'user')
