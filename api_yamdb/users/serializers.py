import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .validators import CustomValidation
from api_yamdb.settings import ADMIN_EMAIL

ROLES = [
    User.Role.ADMIN.value,
    User.Role.MODERATOR.value,
    User.Role.USER.value,
]


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True,
                                      max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, attrs):
        if attrs['username'].lower() == 'me':
            raise serializers.ValidationError('Username already in use')

        if User.objects.filter(
                username=attrs['username'], email=attrs['email']):
            raise CustomValidation(detail='User is already registered ',
                                   field='Info',
                                   status_code=status.HTTP_200_OK)

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already in use')

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already in use')

        return attrs

    def create(self, validated_data):
        confirmation_code = uuid.uuid4().hex
        validated_data['confirmation_code'] = confirmation_code
        send_mail(
            'Confirmation code',
            f'Ваш код подтверждения: {confirmation_code}',
            ADMIN_EMAIL,
            [validated_data.get('email')],
            fail_silently=False,
        )
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True,
                                      max_length=150)
    confirmation_code = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            raise CustomValidation(detail='Invalid confirmation code',
                                   field='confirmation_code',
                                   status_code=status.HTTP_400_BAD_REQUEST)

        attrs['user'] = user
        return attrs

    def get_token(self, obj):
        user = obj['user']
        return str(AccessToken.for_user(user))

    def create(self, validated_data):
        user = validated_data['user']
        token = AccessToken.for_user(user)
        return {'username': user, 'token': token}


class UsersListSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True,
                                      max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already in use')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already in use')
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True,
                                      max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    bio = serializers.CharField()

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class AdminSerializer(ProfileSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = None

    def validate(self, attrs):
        if 'role' in attrs.keys():
            if attrs.get('role') in ROLES:
                return attrs
            raise CustomValidation(
                detail='You do not have permission to perform this action.',
                field='role',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return attrs
