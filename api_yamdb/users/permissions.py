from rest_framework.permissions import SAFE_METHODS, BasePermission

from api_yamdb.settings import ADMIN, MODERATOR, USER


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.is_superuser)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.role == ADMIN)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.role == MODERATOR)


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.role == USER)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id is not None)

    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        return bool(request.user == obj.author)
