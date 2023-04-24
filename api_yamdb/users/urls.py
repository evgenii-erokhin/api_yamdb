from django.urls import include, path
from rest_framework import routers

from .views import (SignUpViewSet, TokenViewSet,
                    UsersListViewSet, AdminViewSet, ProfileViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('auth/signup', SignUpViewSet)
v1_router.register('auth/token', TokenViewSet)
v1_router.register('users', UsersListViewSet)
v1_router.register(r'users', AdminViewSet,
                   basename='users/<username>')
v1_router.register('users/me', ProfileViewSet, basename='users/me')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
