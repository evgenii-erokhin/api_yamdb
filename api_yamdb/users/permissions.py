from rest_framework.permissions import IsAdminUser
from .models import User


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        user = User.objects.get(id=f'{request.user.id}')
        return bool(request.user and user.role == 'admin')
