from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from katalog.models import Product

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmark/bookmark_list.html', {'bookmarks': bookmarks})

@login_required
def add_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Bookmark.objects.get_or_create(user=request.user, product=product)
    return redirect('katalog:product_list')

@login_required
def remove_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Bookmark.objects.filter(user=request.user, product=product).delete()
    return redirect('bookmark:bookmark_list')