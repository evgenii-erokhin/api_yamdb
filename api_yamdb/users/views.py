from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import User
from .permissions import IsAdmin
from .serializers import (AdminSerializer, ProfileSerializer, SignUpSerializer,
                          TokenSerializer, UsersListSerializer)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer


class UsersListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class AdminViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = AdminSerializer
    permission_classes = [IsAdmin]
    pagination_class = None
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProfileViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
