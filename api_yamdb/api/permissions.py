from rest_framework import permissions


class IsAdminOrAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_staff
            or request.user and obj.author
        )
