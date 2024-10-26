from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from katalog.models import Product
from django.http import JsonResponse
from django.db.utils import OperationalError
from django.views.decorators.http import require_POST
from katalog.services import get_all_rows
import json
from django.views.decorators.csrf import csrf_exempt
import urllib.parse

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    bookmark_data = []

    for bookmark in bookmarks:
        if bookmark.product:
            # It's a database product
            product_data = {
                'id': bookmark.product.id,
                'name': bookmark.product.item,
                'price': bookmark.product.price,
                'image_url': bookmark.product.picture_link,
            }
        else:
            # It's a dataset product
            product_data = {
                'id': bookmark.product_id,
                'name': bookmark.product_data['Nama Produk'],
                'price': bookmark.product_data['Harga'],
                'image_url': bookmark.product_data['Link Foto'],
            }
        bookmark_data.append(product_data)

    return render(request, 'bookmark_list.html', {'bookmarks': bookmark_data})


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
def is_bookmarked(request, product_id):
    is_bookmarked = Bookmark.objects.filter(user=request.user, product_id=product_id).exists()
    return JsonResponse({'is_bookmarked': is_bookmarked})

@login_required
@csrf_exempt
@require_POST
def toggle_bookmark(request, product_id):
    try:
        sheet_products = get_all_rows("DATASET PBP7")
        
        if product_id < 0 or product_id >= len(sheet_products):
            return JsonResponse({'error': 'Invalid product ID'}, status=400)
        
        product_data = sheet_products[product_id]
        
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            external_product_id=str(product_id),
            defaults={'product_data': product_data}
        )

        if not created:
            bookmark.delete()
            is_bookmarked = False
        else:
            is_bookmarked = True

        return JsonResponse({'is_bookmarked': is_bookmarked})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
