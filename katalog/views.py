from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from .models import Product  # Assuming Product is your model

# Create your views here.
def show_katalog(request):
    context = {
        'nama': request.user.username,
        'name' : 'Jeremi Felix Adiyatma',
        'npm' : '2306219575',
        'kelas' : 'PBP B',
        'item' : 'Gitar Michael jackson',
        'price' : 600000,
        'description' : 'this is the guitar that Michael Jackson used on his tour in early 2009 months before he died',
    }

    return render(request, "main.html", context)
@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    # Extracting and sanitizing POST data
    item = strip_tags(request.POST.get("item"))
    description = strip_tags(request.POST.get("description"))
    picture_link = request.POST.get("picture_link")
    restaurant = strip_tags(request.POST.get("restaurant"))
    price = request.POST.get("price")
    user = request.user

    # Creating and saving the new product
    new_product = Product(
        item=item,
        description=description,
        picture_link=picture_link,
        restaurant=restaurant,  # New field
        price=price,
        user=user
    )
    new_product.save()

    # Returning a successful response
    return HttpResponse(b"CREATED", status=201)