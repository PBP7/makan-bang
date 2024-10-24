from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Bookmark
import json
from katalog.models import Product

@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)

        bookmark, created = Bookmark.objects.get_or_create(user=request.user, product=product)

        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False})
        
        return JsonResponse({'bookmarked': True})

@login_required
def bookmarked_products(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    products = [bookmark.product for bookmark in bookmarks]
    return render(request, 'bookmarks.html', {'products': products})