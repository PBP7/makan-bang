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

# Create your views here.
def show_katalog(request):
    # Get sorting order from query parameters (default is ascending)
    sort_order = request.GET.get('sort', 'asc')

    # Retrieve and sort the products based on the sort_order
    if sort_order == 'desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all().order_by('price')

    # Add sorted products to context
    context = {
        'nama': request.user.username,
        'products': products,
        'sort_order': sort_order,  # Pass the sort_order to the template for dropdown state
    }

    return render(request, "katalog.html", context)

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    # Extracting and sanitizing POST data
    item = strip_tags(request.POST.get("item"))
    description = strip_tags(request.POST.get("description"))
    picture_link = request.POST.get("picture_link")
    restaurant = strip_tags(request.POST.get("restaurant"))
    price = request.POST.get("price")
    kategori = strip_tags(request.POST.get("kategori"))
    lokasi = strip_tags(request.POST.get("lokasi"))
    nutrition = strip_tags(request.POST.get("nutrition"))
    link_gofood = request.POST.get("link_gofood")
    user = request.user

    # Creating and saving the new product with all required fields
    new_product = Product(
        item=item,
        description=description,
        picture_link=picture_link,
        restaurant=restaurant,
        price=price,
        kategori=kategori,  # New field
        lokasi=lokasi,  # New field
        nutrition=nutrition,  # New field
        link_gofood=link_gofood,  # New field
        user=user
    )
    new_product.save()

    # Returning a successful response
    return HttpResponse(b"CREATED", status=201)

def delete_product_entry(request, id):
    # Get mood berdasarkan id
    product_entry = Product.objects.get(pk = id)
    # Hapus mood
    product_entry.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('katalog:show_katalog'))

def edit_product_entry(request, id):
    # Get mood entry berdasarkan id
    product_entry = Product.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = ProductEntryForm(request.POST or None, instance=product_entry)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('katalog:show_katalog'))

    context = {'form': form}
    return render(request, "edit_product_entry.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
