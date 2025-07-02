from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint

from products.models import Product
from users.models import User

class Review(models.Model):
    content = models.TextField(verbose_name='Содержимое отзыва', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор отзыва')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки отзыва')

    def __str__(self):
        return f'Отзыв {self.user.username} на товар {self.product.name} | id{self.pk}'

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_review_on_product'
            )
        ]
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-time_created',)
