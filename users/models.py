from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_images', blank=True, null=True, verbose_name='Аватар профиля')
    email = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Почта')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
