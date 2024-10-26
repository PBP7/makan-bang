from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from katalog.models import Product
from rateNreview.models import Rating, Review
from django.shortcuts import render, redirect, reverse   
from katalog.forms import ProductEntryForm
from katalog.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Exists, OuterRef
from django.http import HttpResponseBadRequest
from .models import Review
from katalog.services import get_all_rows  # Import the function to get data from Google Sheets

@csrf_exempt
def submit_rating(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        rating_value = request.POST.get('rating')

        product = Product.objects.get(pk=product_id)
        user = request.user

        # Ensure user can only rate once
        if Rating.objects.filter(product=product, user=user).exists():
            return JsonResponse({'error': 'You have already rated this product.'}, status=400)

        rating = Rating.objects.create(product=product, user=user, rating=rating_value)

        # Calculate new average rating
        ratings = Rating.objects.filter(product=product)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

        return JsonResponse({'average_rating': average_rating})

@csrf_exempt
def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        review_text = request.POST.get('review_text')

        product = Product.objects.get(id=product_id)
        user = request.user

        review = Review.objects.create(product=product, user=user, review_text=review_text)

        return JsonResponse({'username': user.username, 'review_text': review_text})




@login_required
def show_rateNreview(request):
    rated_products = Rating.objects.filter(user=request.user, product=OuterRef('pk'))
    products = Product.objects.annotate(has_rated=Exists(rated_products))
    unrated_products = products.filter(has_rated=False)
    user_reviews = Rating.objects.filter(user=request.user)
    
    return render(request, 'rateNreview.html', {'products': unrated_products, 'user_reviews': user_reviews})

    

def product_reviews(request, product_id):
    # Get the product, or return 404 if it doesn’t exist
    product = get_object_or_404(Product, pk=product_id)

    # Calculate the average rating
    average_rating =  Rating.objects.filter(product=product, user=request.user).first().rating

    # Retrieve all reviews for this product
    reviews = Review.objects.filter(product=product).select_related('user')
    reviews_data = [{
        'user': review.user.username,
        'review_text': review.review_text
    } for review in reviews]

    # Return product info along with reviews in JSON format
    return JsonResponse({
        'kategori': product.kategori,
        'lokasi': product.lokasi,
        'rating': average_rating,
        'reviews': reviews_data,
    })


@login_required
def add_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_source = request.POST.get('product_source')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        if not review_text:
            return HttpResponseBadRequest("Review text cannot be empty.")

        if product_source == 'local':
            product = get_object_or_404(Product, pk=product_id.split('_')[1])
        else:  # product_source == 'sheet'
            sheet_products = get_all_rows("DATASET PBP7")
            product_index = int(product_id.split('_')[1])
            product_data = sheet_products[product_index]
            product = {
                'name': product_data['Nama Produk'],
                'restaurant': product_data['Restoran'],
                'category': product_data['Kategori']
            }

        # Create the review
        Review.objects.create(
            user=request.user,
            product_name=product['name'] if isinstance(product, dict) else product.item,
            restaurant=product['restaurant'] if isinstance(product, dict) else product.restaurant,
            category=product['category'] if isinstance(product, dict) else product.kategori,
            rating=rating,
            review_text=review_text
        )

        return redirect('rateNreview:show_rateNreview')
    return HttpResponseForbidden("Invalid request method.")

@login_required
def edit_review(request, product_id):  # Ensure consistent naming here
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        # Get the product and user's rating/review
        product = get_object_or_404(Product, pk=product_id)
        rating_obj = get_object_or_404(Rating, user=request.user, product=product)
        
        # Update the rating value
        rating_obj.rating = rating
        rating_obj.save()
        
        # Update the review text
        review_obj = Review.objects.filter(user=request.user, product=product).first()
        if review_obj:
            review_obj.review_text = review_text
            review_obj.save()
        
        return JsonResponse({'success': True, 'message': "Review updated successfully"})
    return JsonResponse({'success': False, 'message': "Invalid request method"})



@require_POST
def submit_all_changes(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    rating_value = request.POST.get('rating')

    # Update or create the rating
    Rating.objects.update_or_create(
        product=product, user=request.user, defaults={'rating': rating_value}
    )

    # Update existing reviews
    for key, value in request.POST.items():
        if key.startswith('review_'):
            review_id = key.split('_')[1]
            review = get_object_or_404(Review, pk=review_id, product=product, user=request.user)
            review.review_text = value
            review.save()

    # Add new reviews
    new_reviews = request.POST.getlist('new_reviews')
    for text in new_reviews:
        if text.strip():
            Review.objects.create(product=product, user=request.user, review_text=text)

    return JsonResponse({'success': True})

@require_POST
@login_required
def delete_review(request, product_id):
    review = get_object_or_404(Review, product_id=product_id, user=request.user)
    if request.method == 'POST' and request.is_ajax():
        review.delete()
        return JsonResponse({'success': True, 'message': "Review deleted successfully"})
    return JsonResponse({'success': False, 'message': "Invalid request"})







def show_review(request):
    # Fetch local products
    local_products = Product.objects.all()
    
    # Fetch products from Google Sheets
    sheet_products = get_all_rows("DATASET PBP7")
    
    # Combine and format all products
    all_products = [
        {
            'id': f"local_{product.id}",
            'name': product.item,
            'picture_link': product.picture_link,
            'restaurant': product.restaurant,
            'category': product.kategori,
        }
        for product in local_products
    ] + [
        {
            'id': f"sheet_{index}",
            'name': product['Nama Produk'],
            'picture_link': product['Link Foto'],
            'restaurant': product['Restoran'],
            'category': product['Kategori'],
        }
        for index, product in enumerate(sheet_products)
    ]
    
    context = {
        'products': all_products,
    }
    return render(request, 'rateNreview.html', context)

@login_required
def add_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        # Determine if it's a local or sheet product
        if product_id.startswith('local_'):
            product = Product.objects.get(id=product_id.split('_')[1])
            product_name = product.item
            restaurant = product.restaurant
            category = product.kategori
        else:  # sheet product
            sheet_products = get_all_rows("DATASET PBP7")
            index = int(product_id.split('_')[1])
            product = sheet_products[index]
            product_name = product['Nama Produk']
            restaurant = product['Restoran']
            category = product['Kategori']
        
        # Create and save the review
        review = Review(
            user=request.user,
            product_name=product_name,
            restaurant=restaurant,
            category=category,
            rating=rating,
            review_text=review_text
        )
        review.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
