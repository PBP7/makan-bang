from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookmark.models import Bookmark
from katalog.models import Product
from django.http import JsonResponse

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

