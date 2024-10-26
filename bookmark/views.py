from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from katalog.models import Product
from django.http import JsonResponse
import json

def bookmark_list(request):
    # Ambil produk yang dibookmark oleh pengguna saat ini
    bookmarks = Product.objects.filter(user=request.user)
    return render(request, 'bookmark_list.html', {'bookmarks': bookmarks})


@login_required
def remove_bookmark(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    Bookmark.objects.filter(user=request.user, product=product).delete()
    return redirect('bookmark:bookmark_list')

@login_required
def add_bookmark(request, product_id):
    if request.method == "POST":
        data = json.loads(request.body)
        product = get_object_or_404(Product, product_id=product_id)
        with open("path/to/bookmark_list.html", "a") as file:
            file.write(f"<div>{product_id}</div>")
        
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@login_required
def toggle_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.bookmark.all():
        # Jika produk sudah dibookmark oleh user, maka hapus bookmark
        product.bookmark.remove(request.user)
        bookmarked = False
    else:
        # Jika belum dibookmark, tambahkan bookmark
        product.bookmark.add(request.user)
        bookmarked = True
    return JsonResponse({"bookmarked": bookmarked})