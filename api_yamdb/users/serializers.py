import uuid

from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, attrs):
        try:
            user, created = User.objects.get_or_create(**attrs)

            if created:
                raise serializers.ValidationError(
                    "Invalid username or email"
                )

        except IntegrityError:
            raise serializers.ValidationError(
                "User with this username or email already exists")

    def create(self, validated_data):
        confirmation_code = uuid.uuid4().hex
        validated_data['confirmation_code'] = confirmation_code
        user = User.objects.create(**validated_data)
        send_mail(
            'Confirmation code',
            f'Ваш код подтверждения: {confirmation_code}',
            'from@example.com',
            [validated_data.get('email')],
            fail_silently=False,
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    confirmation_code = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        try:
            user, created = User.objects.get_or_create(**attrs)

            if created:
                raise serializers.ValidationError(
                    "Invalid username or confirmed code"
                )

        except IntegrityError:
            raise serializers.ValidationError(
                "User with this username and confirmed code is not exists")
        attrs['token'] = AccessToken.for_user(user)
        return attrs

    def create(self, validated_data):
        return validated_data


class UsersListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
