from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель кастомизированного пользователя.
    Необязательное поле password, необходимое только для суперюзера.
    """
    USER_ROLE = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE,
        default='user'
    )

    class Meta:
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)
