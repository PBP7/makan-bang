# Generated by Django 5.1.2 on 2024-10-24 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("katalog", "0001_initial"),
        ("meal_planning", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mealplan",
            name="food_items",
        ),
        migrations.CreateModel(
            name="MealItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "food_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="katalog.product",
                    ),
                ),
                (
                    "meal_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meal_items",
                        to="meal_planning.mealplan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meal Item",
                "verbose_name_plural": "Meal Items",
            },
        ),
    ]
