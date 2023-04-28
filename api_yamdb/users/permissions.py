from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import User


class IsAdmin(BasePermission):
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


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(request.user and user.role == 'moderator')


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id is not None)

    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user = User.objects.get(id=request.user.id)
        return bool(user == obj.author)
