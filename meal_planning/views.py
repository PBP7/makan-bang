from django.shortcuts import render, redirect  # Pastikan redirect juga diimpor
from django.views import View
from datetime import datetime
import calendar
from katalog.models import Product  # Impor model Product
from .models import MealPlan  # Impor model MealPlan
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from .forms import MealPlanForm 



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
    
@login_required
def finish_meal_plan(request):
    if request.method == 'POST':
        # Ambil data dari form (date, meal type, time)
        selected_date = request.POST.get('selected_date')
        meal_type = request.POST.get('meal')
        meal_time = request.POST.get('time')

        # Ambil meal plan user atau buat yang baru
        meal_plan, created = MealPlan.objects.get_or_create(user=request.user, date=selected_date, meal_type=meal_type, time=meal_time)

        # Tambahkan item makanan ke meal plan jika ada
        food_items = Product.objects.filter(id__in=request.session.get('food_items', []))
        for food_item in food_items:
            meal_plan.food_items.add(food_item)

        # Hapus sesi untuk food items setelah selesai
        request.session['food_items'] = []

        # Redirect ke halaman Create Plan setelah finish
        return redirect(reverse('create_plan'))  # Ganti dengan URL 'create_plan'

    return HttpResponse('Invalid request', status=400)

@login_required
def create_plan(request):
    # Ambil semua meal plan yang dibuat oleh user yang sedang login
    meal_plans = MealPlan.objects.filter(user=request.user)

    # Kirim meal plans ke template
    return render(request, 'create_plan.html', {'meal_plans': meal_plans})


 # Asumsikan kamu sudah membuat form untuk MealPlan

@login_required
def edit_meal_plan(request, id):
    # Ambil meal plan yang akan di-edit berdasarkan id
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)

    if request.method == 'POST':
        # Jika request-nya POST, update data meal plan
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect('create_plan')  # Redirect ke halaman list meal plan setelah berhasil update
    else:
        # Jika request-nya GET, tampilkan form dengan data meal plan
        form = MealPlanForm(instance=meal_plan)

    # Render template dengan form
    return render(request, 'edit_meal_plan.html', {'form': form, 'meal_plan': meal_plan})

@login_required
def delete_meal_plan(request, id):
    # Ambil meal plan yang akan dihapus berdasarkan id
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)

    if request.method == 'POST':
        # Hapus meal plan dan redirect ke halaman list meal plan
        meal_plan.delete()
        return redirect('create_plan')

    # Jika request-nya GET, tampilkan halaman konfirmasi penghapusan
    return render(request, 'confirm_delete.html', {'meal_plan': meal_plan})
