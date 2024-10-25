from django.db import models
from django.contrib.auth.models import User
from katalog.models import Product
from django.utils import timezone

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relasi ke pengguna
    food_items = models.ManyToManyField(Product)  # Relasi ke produk makanan
    date = models.DateField(default=timezone.now) 
    meal_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)  # Menyimpan waktu saat rencana dibuat
    updated_at = models.DateTimeField(auto_now=True)  # Menyimpan waktu saat rencana diperbarui
    time = models.TimeField(null=False) 



