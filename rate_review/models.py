import uuid
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from katalog.models import Product # Import model Produk dari aplikasi katalog

class RateReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rate = models.IntegerField()  # Rating dalam skala 1-5
    review_text = models.TextField(blank=True, null=True)  # Review teks (opsional)
    date = models.DateTimeField(auto_now_add=True)  # Tanggal otomatis

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.rate}/5"

    def clean(self):
        # Validasi rating agar berada di antara 1 hingga 5
        if self.rate < 1 or self.rate > 5:
            raise ValidationError('Rating harus antara 1 hingga 5 bintang.')
