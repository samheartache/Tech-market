# Generated by Django 5.2 on 2025-04-14 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Почта'),
        ),
    ]
