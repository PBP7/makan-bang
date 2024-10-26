from django.forms import ModelForm
from ratenreview.models import Review, Rating

class ReviewEntryForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review_text"]

class RatingEntryForm(ModelForm):
    class Meta:
        model = Rating
        fields = ["rating"]
