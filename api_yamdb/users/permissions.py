from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)
from .models import User


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'admin')


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class IsAdminOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(user.role == 'admin' or user == obj.author)


class IsAuthorOrModer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(user.role == 'moderator' or user == obj.author)
 