from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rate_review.models import RateReview
from rate_review.forms import RateReviewForm    
from katalog.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Avg  # Ini yang benar untuk agregasi rata-rata
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone


@login_required(login_url="authentication:login")
def submit_review(request, id):
    product = get_object_or_404(Product, id=id)

    # Cek jika user sudah memberikan review untuk produk ini
    if RateReview.objects.filter(user=request.user, product=product).exists():
        return redirect('rate_review:product_detail', id=id)  # Redirect jika sudah ada review

    if request.method == "POST":
        rate = request.POST.get('rate')
        review_text = request.POST.get('review_text')

        # Buat review baru
        RateReview.objects.create(
            user=request.user,
            product=product,
            rate=rate,
            review_text=review_text
        )
        
        return redirect('rate_review:product_detail', id=id)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()  # Mengambil semua review untuk produk ini

    # Hitung rata-rata rating dan total rating per bintang
    total_reviews = reviews.count()
    if total_reviews > 0:
        average_rate = reviews.aggregate(Avg('rate'))['rate__avg']
        star_counts = {
            i: reviews.filter(rate=i).count() for i in range(1, 6)
        }
    else:
        average_rate = 0
        star_counts = {i: 0 for i in range(1, 6)}
    filled_percentage = (average_rate - int(average_rate)) * 100

    # Cek jika user sudah pernah review produk ini
    if request.user.is_authenticated:
        user_has_reviewed = RateReview.objects.filter(user=request.user, product=product).exists()
    else:
        user_has_reviewed = False

    return render(request, 'product_detail.html', {
        "product": product,
        'reviews': reviews,
        'average_rate': average_rate,
        'star_counts': star_counts,
        'total_reviews': total_reviews,
        'filled_percentage': filled_percentage,
        'user_has_reviewed': user_has_reviewed,  # Status untuk menampilkan form atau tidak
    })

@login_required(login_url="authentication:login")
def user_rating(request):
    # Mendapatkan semua review yang dibuat oleh user yang sedang login
    user_reviews = RateReview.objects.filter(user=request.user)
    context = {
        'user_reviews': user_reviews,
    }
    return render(request, 'user_rating.html', context)

@csrf_exempt
@login_required(login_url="authentication:login")
def delete_review(request, review_id):
    review = get_object_or_404(RateReview, id=review_id, user=request.user)

    review.delete()
    return HttpResponseRedirect(reverse('rate_review:product_detail', args=[review.product.id]))

@csrf_exempt
@login_required(login_url="authentication:login")
def edit_review(request, review_id):
    review = get_object_or_404(RateReview, id=review_id)
    product = get_object_or_404(Product, id=review.product_id)  # Ambil produk terkait dengan review

    if request.method == 'POST':
        form = RateReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('rate_review:product_detail', id=review.product_id)  # Ganti dengan nama URL yang sesuai
    else:
        form = RateReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review, 'product': product})  # Sertakan product dalam konteks

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
