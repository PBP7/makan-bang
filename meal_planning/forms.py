from django import forms
from .models import MealPlan
from katalog.models import Product

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['date', 'time', 'food_items']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'food_items': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        meal_plan_instance = kwargs.get('instance', None)
        super(MealPlanForm, self).__init__(*args, **kwargs)
        
        if meal_plan_instance:
            self.fields['food_items'].queryset = meal_plan_instance.food_items.all()
        else:
            self.fields['food_items'].queryset = Product.objects.all()

        self.fields['food_items'].label_from_instance = lambda obj: obj.item
