from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookmark.models import Bookmark
from katalog.models import Product
from django.http import JsonResponse

@login_required(login_url="authentication:login")
def bookmark_list(request):
    bookmarks = request.user.bookmarked_products.all()
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
        
        if request.user in product.bookmark.all():
            product.bookmark.remove(request.user)
            bookmarked = False
        else:
            product.bookmark.add(request.user) 
            bookmarked = True
        
        return JsonResponse({"success": True, "bookmarked": bookmarked})
    return JsonResponse({"success": False}, status=400)

@login_required(login_url="authentication:login")
def toggle_bookmark(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.bookmarked.all():
        product.bookmarked.remove(request.user)
        bookmarked = False
    else:
        product.bookmarked.add(request.user)
        bookmarked = True
    return JsonResponse({"bookmarked": bookmarked})

<<<<<<< HEAD
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
=======
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

>>>>>>> 57768dc6b095887ba0b8374981a2151ad660f53a
