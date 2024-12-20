from django.urls import path
from .views import meal_planning, get_food_items_by_name, delete_meal_plan_django, get_food_items, delete_meal_plan, update_meal_plan, finish_meal_plan_json, add_to_meal_plan, cancel_selection, choices_page, process_choices, finish_meal_plan, create_plan, edit_meal_plan, show_json, get_meal_plan, save_meal_plan # Ensure the correct import

urlpatterns = [
    path('meal-planning/', meal_planning, name='meal_planning'),  
    path('add-to-meal-plan/<uuid:food_item_id>/', add_to_meal_plan, name='add_to_meal_plan'),
    path('meal-plan/<int:id>/edit/', edit_meal_plan, name='edit_meal_plan'),
    path('meal-planning/choices/', choices_page, name='choices_page'),
    path('meal-planning/process-choices/', process_choices, name='process_choices'),
    path('finish', finish_meal_plan, name='finish_meal_plan'),
    path('finish-json/', finish_meal_plan_json, name='finish_meal_plan_json'),
    path('create/', create_plan, name='create_plan'),
    path('cancel-selection/', cancel_selection, name='cancel_selection'),
    path('json/', show_json, name='show_json'),
    path('get-meal-plan/', get_meal_plan),
    path('save-meal-plan/', save_meal_plan),
    path('food-items-by-name/', get_food_items_by_name, name='get_food_items_by_name'),
    path('<int:id>/delete/', delete_meal_plan, name='delete_meal_plan'),
    path('<int:id>/update/', update_meal_plan, name='update_meal_plan'),
    path('get-food-items/', get_food_items, name='get_food_items'),
    path('meal-plan/<int:id>/delete/', delete_meal_plan_django, name='delete_meal_plan_django'),
]
