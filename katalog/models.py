from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Avg

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    item = models.CharField(max_length=50)
    picture_link = models.TextField()
    restaurant = models.CharField(max_length=90)
    kategori = models.CharField(max_length=31)
    lokasi =  models.CharField(max_length=175)
    price = models.PositiveIntegerField()
    nutrition = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    link_gofood = models.TextField()
    bookmarked = models.ManyToManyField(User, related_name="bookmarked_products", blank=True)

    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
