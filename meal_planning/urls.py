from django.urls import path
from .views import meal_planning, add_to_meal_plan, delete_food_item  # Ensure the correct import

urlpatterns = [
    path('meal-planning/', meal_planning, name='meal_planning'),  # URL for meal planning
    path('add-to-meal-plan/<uuid:food_item_id>/', add_to_meal_plan, name='add_to_meal_plan'),
    path('delete_food_item/<uuid:food_item_id>/', delete_food_item, name='delete_food_item'),
    path('create_plan/', add_to_meal_plan, name='create_meal_plan')
]
