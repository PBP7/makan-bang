from django import forms
from .models import RateReview

class RateReviewForm(forms.ModelForm):
    class Meta:
        model = RateReview
        fields = ['rate', 'review_text']
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 5, 'type': 'number'}),
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate < 1 or rate > 5:
            raise forms.ValidationError("Rating harus antara 1 hingga 5 bintang.")
        return rate
