from django.urls import path
from .views import meal_planning

urlpatterns = [
    path('meal-planning/', meal_planning, name='meal_planning'),  # URL yang akan diakses
]
