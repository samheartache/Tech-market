from django.db import models
from django.db.models import Avg


class ProductQuerySet(models.QuerySet):
    def get_best_products(self):
        return self.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__isnull=False).order_by('-avg_rating')[:3]


class Product(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, max_length=50, verbose_name='URL')
    description = models.TextField(default='У товара пока нет описания', blank=True, null=True, max_length=500, verbose_name='Описание')
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='product_img', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(to='Category', verbose_name='Категория', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']
    
    objects = ProductQuerySet.as_manager()

    @property
    def average_rating(self):
        from reviews.models import Review
        
        ratings = Review.objects.filter(product=self).values_list('rating', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        return 0


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'