# Generated by Django 4.2.16 on 2024-10-26 09:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('katalog', '0002_alter_product_description_alter_product_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, related_name='bookmarked_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
