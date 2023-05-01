from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import User
from .permissions import IsAdmin, IsModerator, IsSuperUser, IsUser
from .serializers import (AdminSerializer, ProfileSerializer, SignUpSerializer,
                          TokenSerializer, UsersListSerializer)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer


class UsersListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = [IsAdmin | IsSuperUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin | IsSuperUser]
    pagination_class = None
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        user = get_object_or_404(User, id=self.request.user.id)

        if user.role == 'admin':
            return AdminSerializer
        return ProfileSerializer

    @action(detail=True, methods=['get'],
            permission_classes=[IsAdmin | IsSuperUser])
    def get_queryset(self):
        if len(self.kwargs) > 0:
            return User.objects.filter(username=self.kwargs['username'])
        return get_object_or_404(User, id=self.request.user.id)

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdmin | IsSuperUser],
            serializer_class=AdminSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAdmin | IsModerator | IsUser | IsSuperUser],
            url_path='me')
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdmin | IsModerator | IsUser | IsSuperUser],
            url_path='me',
            serializer_class=ProfileSerializer)
    def patch(self, request, *args, **kwargs):
        self.kwargs['username'] = (get_object_or_404(
            User, id=self.request.user.id)).username
        return self.partial_update(request, *args, **kwargs)
