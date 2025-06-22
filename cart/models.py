from django.db import models

from users.models import User
from products.models import Product


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(item.products_price() for item in self)
    
    def total_quantity(self):
        return sum(item.quantity for item in self) if self.exists() else 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    in_order = models.BooleanField(default=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзину'
    
    objects = CartQuerySet.as_manager()

    def products_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f'Товар {self.product.name} в корзине {self.user.username}'
