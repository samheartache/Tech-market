from django.db import models


class Product(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, max_length=20, verbose_name='URL')
    description = models.TextField(default='У товара пока нет описания', max_length=500, verbose_name='Описание')
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to=None, blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey('', verbose_name='Категория', on_delete=models.CASCADE)

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return self.name
    
    class Meta:
        db_tabel = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
