from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.utils import timezone

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


class ViewHistory(models.Model):
    user = models.ForeignKey(to=User, verbose_name='Просмотрено пользователем', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, verbose_name='Просмотренный товар', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    def __str__(self):
        return f'Пользователь {self.user.username} смотрел товар {self.product.name}'
    
    class Meta:
        db_table = 'viewhistory'
        verbose_name = 'История просмотра товаров'
        ordering = ('-time_created',)
    
    @classmethod
    def add_to_history(cls, user, product):
        if not user.is_authenticated:
            return
        
        record, created = cls.objects.get_or_create(
            user=user,
            product=product,
            defaults={'time_created': timezone.now()}
        )

        if not created:
            record.time_created = timezone.now()
            record.save()
        
        history = cls.objects.filter(user=user)
        history_count = history.count()
        if history_count > 4:
            ids_of_newest = history.values_list('id', flat=True)[:4]
            cls.objects.filter(user=user).exclude(id__in=ids_of_newest).delete()