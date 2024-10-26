# Generated by Django 5.1.2 on 2024-10-26 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, related_name='bookmarked_products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='item',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='lokasi',
            field=models.CharField(max_length=175),
        ),
        migrations.AlterField(
            model_name='product',
            name='nutrition',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='restaurant',
            field=models.CharField(max_length=90),
        ),
    ]
