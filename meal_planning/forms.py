from django import forms
from .models import MealPlan

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['date', 'meal_type', 'time', 'food_items']  # Sesuaikan dengan field yang ingin di-edit
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
