from django.db import models
from django.contrib.auth.models import User
from katalog.models import Product
import uuid


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    review_text = models.TextField()


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('product', 'user')  # Mencegah satu user memberi rating lebih dari sekali untuk produk yang sama
