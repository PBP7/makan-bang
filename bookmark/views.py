from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from katalog.models import Product
from django.http import JsonResponse

@login_required
def bookmark_list(request):
    bookmarks = request.user.bookmarked_products.all()
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
        
        if request.user in product.bookmark.all():
            product.bookmark.remove(request.user)
            bookmarked = False
        else:
            product.bookmark.add(request.user) 
            bookmarked = True
        
        return JsonResponse({"success": True, "bookmarked": bookmarked})
    return JsonResponse({"success": False}, status=400)

@login_required
def toggle_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.bookmarked.all():
        product.bookmarked.remove(request.user)
        bookmarked = False
    else:
        product.bookmarked.add(request.user)
        bookmarked = True
    return JsonResponse({"bookmarked": bookmarked})

@login_required
def save_note(request, product_id):
    if request.method == 'POST':
        note = request.POST.get('note')
        print(f"Received note: {note}, for product ID: {product_id}")
        try:
            product = Product.objects.get(id=product_id)
            product.note = note
            product.save()
            print("Note saved successfully.") 
            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            print("Product not found.")
            return JsonResponse({'success': False, 'error': 'Product not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})