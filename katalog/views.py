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
from django.shortcuts import render
from .services import get_all_rows
from django.http import JsonResponse
from django.db.models import Q
import json
from bookmark.models import Bookmark
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def show_katalog(request):
    # Get sorting order from query parameters (default is ascending)
    sort_order = request.GET.get('sort', 'asc')

    # Check if we need to reimport the dataset
    if request.GET.get('reimport') == 'true':
        clear_dataset_products()
    
    # Check if dataset products have been imported
    if not Product.objects.filter(is_dataset_product=True).exists():
        # If not imported, get dataset products and import them to the database
        dataset_products = get_all_rows("DATASET PBP7")
        import_dataset_products(dataset_products)

    # Retrieve and sort all products (including imported ones) based on the sort_order
    if sort_order == 'desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all().order_by('price')

    # user_bookmarks = set(Bookmark.objects.filter(user=request.user).values_list('external_product_id', flat=True))

    # Add all products to context
    context = {
        'nama': request.user.username,
        'products': products,
        'sort_order': sort_order,
    }

    return render(request, "katalog.html", context)

@transaction.atomic
def import_dataset_products(dataset_products):
    # Get or create a default user for dataset products
    default_user, _ = User.objects.get_or_create(username='dataset_importer')
    
    for product in dataset_products:
        Product.objects.create(
            item=product['Nama Produk'],
            restaurant=product['Restoran'],
            user=default_user,
            picture_link=product['Link Foto'],
            lokasi=product['Lokasi'],
            description=product['Deskripsi'],
            price=product['Harga'],
            kategori=product['Kategori'],
            nutrition=product['Nutrisi'],
            link_gofood=product['Link GoFood'],
            is_dataset_product=True,
        )

@transaction.atomic
def clear_dataset_products():
    Product.objects.filter(is_dataset_product=True).delete()

@require_POST
@user_passes_test(lambda u: u.username == 'admin')
def reimport_dataset(request):
    try:
        with transaction.atomic():
            # Clear existing dataset products
            Product.objects.filter(is_dataset_product=True).delete()
            
            # Import new data from Google Sheets
            dataset_products = get_all_rows("DATASET PBP7")
            import_dataset_products(dataset_products)
        
        return JsonResponse({"success": True, "message": "Dataset has been successfully reimported."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

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

def dataset(request):
    products = get_all_rows("DATASET PBP7")
    formatted_products = []
    for product in products:
        formatted_product = {
            'picture_link': product['Link Foto'],
            'item': product['Nama Produk'],
            'restaurant': product['Restoran'],
            'lokasi': product['Lokasi'],
            'description': product['Deskripsi'],
            'price': product['Harga'],
            'kategori': product['Kategori'],
            'nutrition': product['Nutrisi'],
            'link_gofood': product['Link GoFood']
        }
        formatted_products.append(formatted_product)
    return render(request, 'card_product_entry.html', {'product_entries': formatted_products})

def edit(request):
    return redirect('https://docs.google.com/spreadsheets/d/10_JHj928fFrLtnYP9vN8PU7qrf5Y_hXX7gnLIM1BHUw/edit?gid=302655056#gid=302655056')

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(item__icontains=query) |
            Q(kategori__icontains=query) |
            Q(restaurant__icontains=query)
        )
    else:
        products = Product.objects.all()

    product_list = list(products.values())
    return JsonResponse(product_list, safe=False)

def get_all_products(request):
    products = Product.objects.all()
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'item': product.item,
            'pictureLink': product.picture_link,
            'restaurant': product.restaurant,
            'kategori': product.kategori,
            'lokasi': product.lokasi,
            'nutrition': product.nutrition,
            'link_gofood': product.link_gofood,
            'price': float(product.price),
            'description': product.description,
        })
    return JsonResponse(product_list, safe=False)

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            new_product = Product.objects.create(
                user=request.user,
                item=data["item"],
                description=data["description"],
                picture_link=data["picture_link"],
                restaurant=data["restaurant"],
                price=float(data["price"]),
                kategori=data["kategori"],
                lokasi=data["lokasi"],
                nutrition=data["nutrition"],
                link_gofood=data["link_gofood"]
            )

            new_product.save()

            return JsonResponse({
                "status": "success",
                "message": "Product successfully created!"
            }, status=200)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=401)



