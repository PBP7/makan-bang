from django.urls import path
from .views import meal_planning, add_to_meal_plan, delete_food_item, choices_page, process_choices  # Ensure the correct import

urlpatterns = [
    path('meal-planning/', meal_planning, name='meal_planning'),  # URL for meal planning
    path('add-to-meal-plan/<uuid:food_item_id>/', add_to_meal_plan, name='add_to_meal_plan'),
    path('delete_food_item/<uuid:food_item_id>/', delete_food_item, name='delete_food_item'),
    path('meal-planning/choices/', choices_page, name='choices_page'),
     path('meal-planning/process-choices/', process_choices, name='process_choices'),
]
