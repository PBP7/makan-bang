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
from django.core import serializers
import uuid

# Meal Planning Home Page
@login_required(login_url="authentication:login")
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


def get_meal_plan(request):
    user_id = request.GET.get('user')
    meal_plan = MealPlan.objects.filter(user_id=user_id).first()
    if meal_plan:
        data = json.loads(serializers('json', [meal_plan]))
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def save_meal_plan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fields = data.get('fields')
        meal_plan, created = MealPlan.objects.update_or_create(
            pk=data.get('pk'),
            defaults={
                'user_id': fields.get('user'),
                'date': fields.get('date'),
                'time': fields.get('time'),
                'food_items': fields.get('food_items'),
            }
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# Choices Page for Selecting Foods
@login_required(login_url="authentication:login")
def choices_page(request):
    product_entries = Product.objects.all()
    return render(request, 'choices_page.html', {'product_entries': product_entries})
def show_json(request):
    data = []
    meal_plans = MealPlan.objects.all()

    for meal_plan in meal_plans:
        food_items = [
            food.item for food in meal_plan.food_items.all()
        ]
        data.append({
            "model": "mealplan.mealplan",  # Tambahkan nama model
            "pk": meal_plan.id,  # ID MealPlan, bukan ID User
            "fields": {
                "user": meal_plan.user.id,
                "date": meal_plan.date.strftime("%Y-%m-%d"),
                "time": str(meal_plan.time),
                "food_items": food_items
            }
        })

    return JsonResponse(data, safe=False)

# Add Food Item to Meal Plan
@login_required(login_url="authentication:login")
def add_to_meal_plan(request, food_item_id):
    food_item = get_object_or_404(Product, pk=food_item_id)
    meal_plan, created = MealPlan.objects.get_or_create(user=request.user)
    meal_plan.food_items.add(food_item)
    return redirect(reverse('meal_planning'))



# Delete Food Item from Meal Plan
@login_required(login_url="authentication:login")
def delete_food_item(request, food_item_id):
    if request.method == "POST":
        meal_plan = get_object_or_404(MealPlan, user=request.user)
        food_item = get_object_or_404(Product, pk=food_item_id)
        meal_plan.food_items.remove(food_item)
        return redirect('meal_planning')
    return HttpResponse('Invalid request', status=400)

@login_required(login_url="authentication:login")
def cancel_selection(request):
    # Clear the selected foods in session
    if 'selected_foods' in request.session:
        del request.session['selected_foods']
    
    # Redirect to the create_plan page
    return redirect('create_plan')
# Process Choices from the Selection Page and Store in Session
@login_required(login_url="authentication:login")
def process_choices(request):
    if request.method == 'POST':
        selected_foods = request.POST.getlist('selected_foods')
        request.session['selected_foods'] = selected_foods
        return redirect('meal_planning')
    return HttpResponse('Invalid request', status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Gunakan hanya jika Flutter belum mengatur CSRF token
def process_choices_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_foods = data.get('selected_foods', [])
            
            # Simpan pilihan makanan ke session (opsional)
            request.session['selected_foods'] = selected_foods
            
            return JsonResponse({'message': 'Choices processed successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def food_list(request):
    foods = Product.objects.all().values('id', 'name', 'category', 'price', 'picture_url')
    return JsonResponse(list(foods), safe=False)

# Finalize and Save the Meal Plan
@login_required(login_url="authentication:login")
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

@csrf_exempt
def finish_meal_plan_json(request):
    print("masukkkk/....")
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            selected_date = data.get('selected_date')
            meal_time = data.get('time')
            selected_foods = data.get('foodItems', [])

            # Validate required fields
            if not selected_date or not meal_time or not selected_foods:
                return JsonResponse({'error': 'Date, time, and food items are required.'}, status=400)

            # Validate food item IDs as UUIDs
            # try:
            #     selected_foods = [UUID(fid) for fid in selected_foods]
            # except ValueError:
            #     return JsonResponse({'error': 'Invalid UUID format in food items.'}, status=400)

            # Create or get meal plan for the user
            meal_plan = MealPlan.objects.create(
                user=request.user,
                date=selected_date,
                time=meal_time
            )

            # Validate and update food items
            food_items = Product.objects.filter(id__in=selected_foods)
            if not food_items.exists():
                return JsonResponse({'error': 'Invalid food items selected.'}, status=400)

            # Update the meal plan's food items
            meal_plan.food_items.set(food_items)
            meal_plan.save()

            return JsonResponse({
                'message': 'Meal plan created successfully!',
                'status': 'success'
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required(login_url="authentication:login")
def create_plan(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    today = timezone.now().date()

    today_meal_plans = meal_plans.filter(date=today)
    future_meal_plans = meal_plans.filter(date__gt=today).order_by('date') 
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
        'other_meal_plans': future_meal_plans,
        'has_today_plan': has_today_plan,
        'past_meal_plans': past_meal_plans,
    }
    
    return render(request, 'create_plan.html', context)

@login_required(login_url="authentication:login")
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

@login_required(login_url="authentication:login")
@require_POST
def delete_meal_plan(request, id):
    meal_plan = get_object_or_404(MealPlan, id=id, user=request.user)
    meal_plan.delete()
    return JsonResponse({'status': 'success', 'message': 'Meal plan deleted successfully.'})