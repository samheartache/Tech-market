from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_images', blank=True, null=True, verbose_name='Аватар профиля')
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Review(models.Model):
    content = models.TextField(verbose_name='Содержимое отзыва', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор отзыва')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки отзыва')

    def __str__(self):
        return f'Отзыв {self.user.username} на товар {self.product.name} | id{self.pk}'

    class Meta:
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
