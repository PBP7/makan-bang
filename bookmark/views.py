from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookmark.models import Bookmark
from katalog.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
import json
@login_required(login_url="authentication:login")
def bookmark_list(request):
    # Ambil produk yang dibookmark oleh pengguna saat ini
    bookmarks = request.user.bookmarked_products.all()  # Menggunakan related_name dari ManyToManyField
    return render(request, 'bookmark_list.html', {'bookmarks': bookmarks})



@login_required(login_url="authentication:login")
def remove_bookmark(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.bookmarked.remove(request.user)
    return redirect('bookmark:bookmark_list')


@login_required(login_url="authentication:login")
@csrf_exempt
def bookmarked_list(request):
    try:
        # Ambil semua produk yang telah di-bookmark oleh user saat ini
        bookmarked_products = request.user.bookmarked_products.all()  # Gunakan related_name

        # Format data sesuai model Flutter
        products_data = [
            {
                "model": "katalog.product",  # Nama model
                "pk": str(product.pk),  # Primary Key sebagai string
                "fields": {
                    "item": product.item,  # Nama produk
                    "picture_link": product.picture_link,  # Gambar produk
                    "restaurant": product.restaurant,  # Nama restoran
                    "kategori": product.kateogri,  # Kategori produk
                    "lokasi": product.lokasi,  # Lokasi
                    "price": product.price,  # Harga
                    "nutrition": product.nutrition,  # Informasi nutrisi
                    "description": product.description,  # Deskripsi produk
                    "link_gofood": product.link_gofood,  # Link ke GoFood
                    "is_dataset_product": product.is_dataset_product,  # Apakah produk berasal dari dataset
                    "bookmarked": list(product.bookmarked.values_list('id', flat=True)),  # Daftar ID user yang bookmark
                }
            }
            for product in bookmarked_products
        ]

        return JsonResponse({
            "success": True,
            "products": products_data,
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
        }, status=400)

@login_required(login_url="authentication:login")
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

@login_required(login_url="authentication:login")
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

@login_required(login_url="authentication:login")
def add_or_edit_note(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id = product_id)
    note = request.POST.get('note')
    bookmark = get_object_or_404(Bookmark, product = product, user = request.user)

    # Save note to the bookmark
    bookmark.note = note
    bookmark.save()
    
    return JsonResponse({'status': 'success', 'note': bookmark.note})


@csrf_exempt
@login_required(login_url="authentication:login")
def add_bookmark_flutter(request):
    if request.method == "POST":
        try:
            # Parse JSON dari body permintaan
            data = json.loads(request.body)
            product_id = data.get('product_id')  # Ambil ID produk dari JSON
            product = get_object_or_404(Product, id=product_id)
            # Tambahkan bookmark jika user belum menandai produk
            if request.user not in product.bookmarked.all():
                product.bookmarked.add(request.user)
                bookmarked = True
            else:
                bookmarked = False  # Produk sudah dibookmark sebelumnya

            return JsonResponse({
                "success": True,
                "bookmarked": bookmarked,
                "message": "Bookmark added successfully." if bookmarked else "Product already bookmarked."
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
@login_required(login_url="authentication:login")
def delete_bookmark_flutter(request,product_id):
    if request.method == "POST":
        try:
            # Parse JSON dari body permintaan
            data = json.loads(request.body)
            product_id = data.get('product_id')  # Ambil ID produk dari JSON
            product = get_object_or_404(Product, id=product_id)

            # Hapus bookmark jika user sudah menandai produk
            if request.user in product.bookmarked.all():
                product.bookmarked.remove(request.user)
                removed = True
            else:
                removed = False  # Produk belum dibookmark sebelumnya

            return JsonResponse({
                "success": True,
                "removed": removed,
                "message": "Bookmark removed successfully." if removed else "Product was not bookmarked."
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
@csrf_exempt
def toggle_bookmark_flutter(request, product_id):
    user_id = request.user  # atau ID user dari request
    product = Product.objects.get(id=product_id)  # Ambil produk berdasarkan ID
    if user_id in product.bookmarked.all():
        product.bookmarked.remove(user_id)  # Hapus user dari bookmark
        action = False
    else:
        product.bookmarked.add(user_id)  # Tambahkan user ke bookmark
        action = True
    product.save()
    return JsonResponse({
        "success": True,
        "bookmarked": action,
    })




