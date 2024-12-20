from django.urls import path
from .views import meal_planning, add_to_meal_plan, cancel_selection, choices_page, process_choices, finish_meal_plan, create_plan, delete_meal_plan, edit_meal_plan # Ensure the correct import

urlpatterns = [
    path('meal-planning/', meal_planning, name='meal_planning'),  
    path('add-to-meal-plan/<uuid:food_item_id>/', add_to_meal_plan, name='add_to_meal_plan'),
    path('meal-plan/<int:id>/edit/', edit_meal_plan, name='edit_meal_plan'),
    path('meal-plan/<int:id>/delete/', delete_meal_plan, name='delete_meal_plan'),
    path('meal-planning/choices/', choices_page, name='choices_page'),
    path('meal-planning/process-choices/', process_choices, name='process_choices'),
    path('finish', finish_meal_plan, name='finish_meal_plan'),
    path('create/', create_plan, name='create_plan'),
    path('meal-plan/<int:id>/delete/', delete_meal_plan, name='delete_meal_plan'),
    path('cancel-selection/', cancel_selection, name='cancel_selection'),
    

    
    

]
