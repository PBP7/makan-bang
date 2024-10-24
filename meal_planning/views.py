from django.shortcuts import render, redirect  # Pastikan redirect juga diimpor
from django.views import View
from datetime import datetime
import calendar
from katalog.models import Product  # Impor model Product
from .models import MealPlan  # Impor model MealPlan
from django.shortcuts import get_object_or_404, redirect

# Meal Planning View
def meal_planning(request):
    # Get current date
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Get days in the current month
    month_days = calendar.monthcalendar(current_year, current_month)

    # Month name
    month_name = today.strftime('%B')

    # Ambil makanan dari MealPlan
    meal_plan = MealPlan.objects.filter(user=request.user).first()
    food_items = meal_plan.food_items.all() if meal_plan else []

    context = {
        'month_name': month_name,
        'month_days': month_days,
        'current_day': today.day,
        'food_items': food_items,  # Kirim data makanan ke template
    }

    return render(request, 'meal_planning.html', context)


def choices_page(request):
    # Mengambil semua produk dari database
    product_entries = Product.objects.all()
    
    # Render ke template choices_page.html
    return render(request, 'choices_page.html', {'product_entries': product_entries})



def add_to_meal_plan(request, food_item_id):
    food_item = Product.objects.get(pk=food_item_id)
    meal_plan, created = MealPlan.objects.get_or_create(user=request.user)
    meal_plan.food_items.add(food_item)
    return redirect('meal_planning')  # Redirect ke halaman meal planning

def delete_food_item(request, food_item_id):
    if request.method == "POST":
        meal_plan = get_object_or_404(MealPlan, user=request.user)
        food_item = get_object_or_404(Product, pk=food_item_id)
        
        # Hapus food item dari meal plan
        meal_plan.food_items.remove(food_item)
        
        # Redirect setelah penghapusan
        return redirect('meal_planning')



def process_choices(request):
    if request.method == 'POST':
        # Ambil semua makanan yang dipilih dari form
        selected_foods = request.POST.getlist('selected_foods')

        # Iterasi setiap food_item_id yang dipilih
        for food_item_id in selected_foods:
            # Panggil fungsi add_to_meal_plan untuk setiap item
            food_item = get_object_or_404(Product, pk=food_item_id)
            meal_plan, created = MealPlan.objects.get_or_create(user=request.user)
            meal_plan.food_items.add(food_item)
        
        # Setelah menambahkan semua makanan ke meal plan, redirect ke halaman meal planning
        return redirect('meal_planning')  # Redirect ke halaman meal planning atau halaman lain yang diinginkan
