# Generated by Django 4.2.7 on 2025-03-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_img', verbose_name='Изображение'),
        ),
    ]
