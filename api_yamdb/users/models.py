from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'

    base_role = Role.USER

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=base_role
    )
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)
