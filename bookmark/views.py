from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookmark.models import Bookmark
from katalog.models import Product
from django.http import JsonResponse

@login_required
def bookmark_list(request):
    # Ambil produk yang dibookmark oleh pengguna saat ini
    bookmarks = request.user.bookmarked_products.all()  # Menggunakan related_name dari ManyToManyField
    return render(request, 'bookmark_list.html', {'bookmarks': bookmarks})


@login_required
def remove_bookmark(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.bookmarked.remove(request.user)
    return redirect('bookmark:bookmark_list')

@login_required
def add_bookmark(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        
        # Tambahkan atau hapus bookmark berdasarkan status saat ini
        if request.user in product.bookmark.all():
            product.bookmark.remove(request.user)  # Hapus bookmark jika sudah ada
            bookmarked = False
        else:
            product.bookmark.add(request.user)  # Tambahkan bookmark jika belum ada
            bookmarked = True
        
        return JsonResponse({"success": True, "bookmarked": bookmarked})
    return JsonResponse({"success": False}, status=400)

@login_required
def toggle_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.bookmarked.all():
        # Jika produk sudah dibookmark oleh user, maka hapus bookmark
        product.bookmarked.remove(request.user)
        bookmarked = False
    else:
        # Jika belum dibookmark, tambahkan bookmark
        product.bookmarked.add(request.user)
        bookmarked = True
    return JsonResponse({"bookmarked": bookmarked})