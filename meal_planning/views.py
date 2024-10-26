from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from datetime import datetime
import calendar
from katalog.models import Product
from .models import MealPlan
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from .forms import MealPlanForm

def meal_planning(request):
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    selected_foods = request.session.get('selected_foods', [])
    food_items = Product.objects.filter(pk__in=selected_foods)
    month_days = calendar.monthcalendar(current_year, current_month)
    month_name = today.strftime('%B')
    context = {
        'month_name': month_name,
        'month_days': month_days,
        'current_day': today.day,
        'food_items': food_items,
    }
    return render(request, 'meal_planning.html', context)

def choices_page(request):
    product_entries = Product.objects.all()
    return render(request, 'choices_page.html', {'product_entries': product_entries})

def add_to_meal_plan(request, food_item_id):
    food_item = Product.objects.get(pk=food_item_id)
    meal_plan, created = MealPlan.objects.get_or_create(user=request.user)
    meal_plan.food_items.add(food_item)
    return redirect(reverse('meal_planning'))

def delete_food_item(request, food_item_id):
    if request.method == "POST":
        meal_plan = get_object_or_404(MealPlan, user=request.user)
        food_item = get_object_or_404(Product, pk=food_item_id)
        meal_plan.food_items.remove(food_item)
        return redirect('meal_planning')

@login_required
def process_choices(request):
    if request.method == 'POST':
        selected_foods = request.POST.getlist('selected_foods')
        request.session['selected_foods'] = selected_foods
        return redirect('meal_planning')
    return HttpResponse('Invalid request', status=400)

@login_required
def finish_meal_plan(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        meal_time = request.POST.get('time')
        selected_foods = request.session.get('selected_foods', [])
        if not selected_date or not meal_time:
            return HttpResponse('Date and time are required.', status=400)
        meal_plan, created = MealPlan.objects.get_or_create(user=request.user, date=selected_date, time=meal_time)
        food_items = Product.objects.filter(pk__in=selected_foods)
        for food_item in food_items:
            meal_plan.food_items.add(food_item)
        del request.session['selected_foods']
        return redirect(reverse('create_plan'))
    return HttpResponse('Invalid request', status=400)

@login_required
def create_plan(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    return render(request, 'create_plan.html', {'meal_plans': meal_plans})

@login_required
def edit_meal_plan(request, id):
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)
    if request.method == 'POST':
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect('create_plan')
    else:
        form = MealPlanForm(instance=meal_plan)
    return render(request, 'edit_meal_plan.html', {'form': form, 'meal_plan': meal_plan})

@login_required
def delete_meal_plan(request, id):
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)
    if request.method == 'POST':
        meal_plan.delete()
        return redirect('create_plan')
    return render(request, 'confirm_delete.html', {'meal_plan': meal_plan})
