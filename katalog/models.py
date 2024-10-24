from django.db import models
import uuid
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    item = models.CharField(max_length=255)
    picture_link = models.TextField()
    restaurant = models.CharField(max_length=63)
    kategori = models.CharField(max_length = 31)
    lokasi = models.TextField()
    price = models.IntegerField()
    nutrition = models.CharField(max_length = 63)
    description = models.TextField()
    link_gofood =models.TextField()
   