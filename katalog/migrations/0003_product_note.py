# Generated by Django 5.1.2 on 2024-10-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0002_product_bookmarked_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
