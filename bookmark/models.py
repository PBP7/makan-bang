from django.db import models
from django.contrib.auth.models import User
from katalog.models import Product

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    external_product_id = models.CharField(max_length=255, null=True, blank=True)  # For dataset products
    product_data = models.JSONField(null=True, blank=True)  # To store data for dataset products

    class Meta:
        unique_together = ('user', 'product', 'external_product_id')

    def __str__(self):
        if self.product:
            return f"{self.user.username} - {self.product.item}"
        else:
            return f"{self.user.username} - External Product {self.external_product_id}"

# from django.db import models
# from django.contrib.auth.models import User
# from katalog.models import Product

# class Bookmark(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user', 'product')

#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"