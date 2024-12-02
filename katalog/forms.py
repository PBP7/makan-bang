from django.forms import ModelForm
from katalog.models import Product
from django.utils.html import strip_tags

class ProductEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["item","picture_link","restaurant","kategori","lokasi", "price","nutrition", "description","link_gofood"]
        

   