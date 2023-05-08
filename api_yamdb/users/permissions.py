from rest_framework.permissions import SAFE_METHODS, BasePermission

from api_yamdb.settings import ADMIN, MODERATOR, USER


class RolePermission(BasePermission):
    role = None

    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.role == self.role)


class IsSuperUser(RolePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return bool(request.user and request.user.is_superuser)


class IsAdmin(RolePermission):
    role = ADMIN


class IsModerator(RolePermission):
    role = MODERATOR


class IsUser(RolePermission):
    role = USER


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.id is not None
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role in (ADMIN, MODERATOR)
        )
