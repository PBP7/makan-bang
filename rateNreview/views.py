from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from katalog.models import Product
from rateNreview.models import Rating, Review

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
