from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
import calendar
import json
from katalog.models import Product
from .models import MealPlan
from .forms import MealPlanForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

# Meal Planning Home Page
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

# Choices Page for Selecting Foods
def choices_page(request):
    product_entries = Product.objects.all()
    return render(request, 'choices_page.html', {'product_entries': product_entries})

# Add Food Item to Meal Plan
@login_required
def add_to_meal_plan(request, food_item_id):
    food_item = get_object_or_404(Product, pk=food_item_id)
    meal_plan, created = MealPlan.objects.get_or_create(user=request.user)
    meal_plan.food_items.add(food_item)
    return redirect(reverse('meal_planning'))

# Delete Food Item from Meal Plan
@login_required
def delete_food_item(request, food_item_id):
    if request.method == "POST":
        meal_plan = get_object_or_404(MealPlan, user=request.user)
        food_item = get_object_or_404(Product, pk=food_item_id)
        meal_plan.food_items.remove(food_item)
        return redirect('meal_planning')
    return HttpResponse('Invalid request', status=400)

@login_required
def cancel_selection(request):
    # Clear the selected foods in session
    if 'selected_foods' in request.session:
        del request.session['selected_foods']
    
    # Redirect to the create_plan page
    return redirect('create_plan')

# Process Choices from the Selection Page and Store in Session
@login_required
def process_choices(request):
    if request.method == 'POST':
        selected_foods = request.POST.getlist('selected_foods')
        request.session['selected_foods'] = selected_foods
        return redirect('meal_planning')
    return HttpResponse('Invalid request', status=400)

# Finalize and Save the Meal Plan
@login_required
def finish_meal_plan(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        meal_time = request.POST.get('time')
        selected_foods = request.session.get('selected_foods', [])
        
        if not selected_date or not meal_time:
            return HttpResponse('Date and time are required.', status=400)
        
        meal_plan, created = MealPlan.objects.get_or_create(
            user=request.user, date=selected_date, time=meal_time
        )
        
        food_items = Product.objects.filter(pk__in=selected_foods)
        for food_item in food_items:
            meal_plan.food_items.add(food_item)
        
        # Clear selected_foods after use
        if 'selected_foods' in request.session:
            del request.session['selected_foods']
        
        return redirect(reverse('create_plan'))
    
    return HttpResponse('Invalid request', status=400)

# List All Meal Plans
@login_required
def create_plan(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    today = timezone.now().date()

    today_meal_plans = meal_plans.filter(date=today)
    other_meal_plans = meal_plans.exclude(date=today).order_by('date')
    has_today_plan = today_meal_plans.exists()
    past_meal_plans = meal_plans.filter(date__lt=today)

    request.session['show_today_reminder'] = has_today_plan

    meal_plans_data = []
    for meal_plan in meal_plans:
        food_items = list(meal_plan.food_items.values('item'))
        
        meal_plans_data.append({
            'id': meal_plan.id,
            'date': meal_plan.date.strftime('%Y-%m-%d'),
            'time': meal_plan.time.strftime('%H:%M'),
            'food_items': food_items     
        })

    context = {
        'meal_plans': meal_plans,
        'meal_plans_json': json.dumps(meal_plans_data),  # JSON data to be used in JavaScript
        'today_meal_plans': today_meal_plans,
        'other_meal_plans': other_meal_plans,
        'has_today_plan': has_today_plan,
        'past_meal_plans': past_meal_plans,
    }
    
    return render(request, 'create_plan.html', context)

@login_required

def edit_meal_plan(request, id):
    # Get the existing meal plan object based on the ID
    meal_plan = get_object_or_404(MealPlan, id=id)
    
    if request.method == 'POST':
        form = MealPlanForm(request.POST, instance=meal_plan)
        
        if form.is_valid():
            form.save()
            return redirect('create_plan') 
    
    else:
        form = MealPlanForm(instance=meal_plan)
    
    return render(request, 'edit_meal_plan.html', {'form': form, 'meal_plan': meal_plan})

@login_required
@require_POST
def delete_meal_plan(request, id):
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)
    meal_plan.delete()
    return JsonResponse({'status': 'success', 'message': 'Meal plan deleted successfully.'})