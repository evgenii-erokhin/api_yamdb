from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)

from .models import User


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'admin')


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class IsAuthorOrModer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id is not None)

    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(user.role == 'moderator' or user == obj.author)
