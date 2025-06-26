from django.db import models

from users.models import User
from products.models import Product

class OrderProductQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart_prod.products_price() for cart_prod in self)
    
    def total_quantity(self):
        return sum(item.quantity for item in self) if self.exists() else 0


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None, verbose_name='Пользователь')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется ли доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен ли заказ')
    status = models.CharField(max_length=50, default='processing', choices=STATUS_CHOICES, verbose_name='Статус заказа')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('id',)

    def __str__(self):
        return f'Заказ №{self.id} Пользователя: {self.user.username} ({self.user.first_name} {self.user.last_name})'
    

class OrderProduct(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, default=None)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    name = models.CharField(max_length=200, verbose_name='Название продукта')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')

    class Meta:
        db_table = 'orderproduct'
        verbose_name = 'Товар из заказа'
        verbose_name_plural = 'Товары из заказа'

    objects = OrderProductQueryset.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)
    
    def __str__(self):
        return f'Товар из заказа {self.order} | {self.name} Количество: {self.quantity}'
