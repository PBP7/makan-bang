from django.db import models
from django.contrib.auth.models import User
from katalog.models import Product

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relasi ke pengguna
    food_items = models.ManyToManyField(Product)  # Relasi ke produk makanan
    created_at = models.DateTimeField(auto_now_add=True)  # Menyimpan waktu saat rencana dibuat
    updated_at = models.DateTimeField(auto_now=True)  # Menyimpan waktu saat rencana diperbarui

    class Meta:
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'

    def __str__(self):
        return f"{self.user.username}'s Meal Plan"
