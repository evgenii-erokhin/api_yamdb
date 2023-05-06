from http import HTTPStatus

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
    queryset = User.objects.all()
    permission_classes = [IsAdmin | IsSuperUser]
    pagination_class = None
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if ((self.request.user.role == 'admin')
                or self.request.user.is_superuser):
            return AdminSerializer
        return ProfileSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(username=self.kwargs.get('username'))
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdmin | IsSuperUser],
            serializer_class=AdminSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAdmin | IsModerator | IsUser | IsSuperUser],
            url_path='me')
    def me(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdmin | IsModerator | IsUser | IsSuperUser],
            url_path='me',
            serializer_class=ProfileSerializer)
    def patch(self, request, *args, **kwargs):
        self.kwargs['username'] = request.user.username
        return self.partial_update(request, *args, **kwargs)
