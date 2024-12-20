from django.db import models
from django.contrib.auth.models import User
from katalog.models import Product
from django.utils import timezone

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(Product)
    date = models.DateField(default=timezone.now) 
    time = models.TimeField(default="12:00:00")
