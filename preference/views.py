from django.shortcuts import render,redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from preference.forms import PreferenceForm
from preference.models import Preference
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from katalog.models import Product  # Import the Product model
import uuid
from katalog.services import get_all_rows
import re


# Create your views here.
@login_required(login_url="authentication:login")
def show_preference(request):
    preference_entries = Preference.objects.filter(user=request.user)  
    form = PreferenceForm()
    
    context = {
        'preference_entries': preference_entries,
        'form': form 
    }
    return render(request, "add_preference.html", context)

@login_required(login_url="authentication:login")
def preference_page(request):
    preferences = Preference.objects.filter(user=request.user)
    context = {
        'preferences': preferences,
    }
    return render(request, 'preference.html', context)

@login_required(login_url="authentication:login")
@csrf_exempt
@require_POST
def add_preference_ajax(request):
    if request.method == "POST":
        preference_name = strip_tags(request.POST.get("preference_name"))
        user = request.user

        # Check for a valid preference name
        if preference_name:
            # Create and save the new preference
            new_preference = Preference(preference=preference_name, user=user)
            new_preference.save()

            # Return a JSON response
            return JsonResponse({"status": "success", "id": new_preference.id, "preference_name": new_preference.preference}, status=201)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required(login_url="authentication:login")
@require_POST
def delete_preference_ajax(request, preference_id):
    try:
        preference = Preference.objects.get(id=preference_id, user=request.user)
        preference.delete()
        return JsonResponse({"status": "success"})
    except Preference.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Preference not found"}, status=404)

@login_required(login_url="authentication:login")
def get_preferences(request):
    """Return the updated preferences list as HTML for AJAX requests."""
    preferences = Preference.objects.filter(user=request.user)
    html = render_to_string('preference_list.html', {'preference_entries': preferences}, request=request)
    return JsonResponse({'html': html})

@login_required(login_url="authentication:login")
def get_products(request):
    preferences = Preference.objects.filter(user=request.user).values_list('preference', flat=True)
    products = Product.objects.filter(item__in=preferences)

    html = render_to_string('preference.html', {'product_entries': products}, request=request)
    return JsonResponse({'html': html})

@login_required(login_url="authentication:login")
def add_preference(request):
    if request.method == 'POST':
        preference = request.POST.get('preference_name')
        if preference:
            new_preference = Preference.objects.create(user=request.user, preference=preference)
            return JsonResponse({
                'status': 'success',
                'id': new_preference.id,
                'preference_name': new_preference.preference
            })
    return JsonResponse({'status': 'error'})

@login_required(login_url="authentication:login")
@require_http_methods(["DELETE"])
def delete_preference(request, preference_id):
    try:
        preference = Preference.objects.get(id=preference_id, user=request.user)
        preference.delete()
        return JsonResponse({'status': 'success'})
    except Preference.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Preference not found'}, status=404)

@login_required(login_url="authentication:login")
def show_preferences(request):
    preferences = Preference.objects.filter(user=request.user)
    context = {
        'preferences': preferences,
    }
    return render(request, 'preference.html', context)

@login_required(login_url="authentication:login")
def get_filtered_products(request):
    preferences = Preference.objects.filter(user=request.user).values_list('preference', flat=True)
    
    matching_products = Product.objects.none()
    for pref in preferences:
        matching_products |= Product.objects.filter(
            Q(item__icontains=pref) |
            Q(description__icontains=pref) |
            Q(kategori__icontains=pref) |
            Q(restaurant__icontains=pref)
        )
    
    products_data = [{
        'pk': product.pk,
        'item': product.item,
        'picture_link': product.picture_link,
        'time': str(product.time),
        'price': str(product.price),
        'restaurant': product.restaurant,
        'lokasi': product.lokasi,
        'kategori': product.kategori,
        'description': product.description,
        'link_gofood': product.link_gofood,
    } for product in matching_products]
    
    return JsonResponse(products_data, safe=False)

@login_required(login_url="authentication:login")
def get_matching_products(request):
    try:
        user_preferences = Preference.objects.filter(user=request.user).values_list('preference', flat=True)
        
        # Get products from Google Spreadsheet
        spreadsheet_products = get_all_rows("DATASET PBP7")
        
        matching_products = []
        for product in spreadsheet_products:
            # Create a combined string of all relevant fields for searching
            search_string = ' '.join([
                product.get('Nama Produk', ''),
                product.get('Deskripsi', ''),
                product.get('Kategori', ''),
                product.get('Restoran', ''),
                product.get('Lokasi', '')
            ]).lower()
            
            # Check if any preference matches any part of the search string
            if any(re.search(r'\b' + re.escape(pref.lower()) + r'\b', search_string) for pref in user_preferences):
                matching_products.append({
                    'name': product.get('Nama Produk', ''),
                    'description': product.get('Deskripsi', ''),
                    'price': product.get('Harga', ''),
                    'kategori': product.get('Kategori', ''),
                    'picture_link': product.get('Link Foto', ''),
                    'restaurant': product.get('Restoran', ''),
                    'lokasi': product.get('Lokasi', ''),
                    'nutrition': product.get('Nutrition', 'Not available'),  # Provide a default value
                    'link_gofood': product.get('Link GoFood', ''),
                })
        
        return JsonResponse(matching_products, safe=False)
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_matching_products: {str(e)}")
        return JsonResponse({'error': 'An error occurred while fetching matching products'}, status=500)
