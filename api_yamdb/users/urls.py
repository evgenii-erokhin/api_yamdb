from django.urls import include, path
from rest_framework import routers

from .views import SignUpViewSet, TokenViewSet, UsersListViewSet, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register('auth/signup', SignUpViewSet,
                   basename='/api/v1/auth/signup/')
v1_router.register('auth/token', TokenViewSet,
                   basename='/api/v1/auth/token/')
v1_router.register('users', UsersListViewSet)
v1_router.register('users', UserViewSet,
                   basename='/users/<username>/')


urlpatterns = [
    path('v1/', include(v1_router.urls)),

]
