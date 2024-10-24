from django.urls import path
from rateNreview.views import submit_rating, submit_review
app_name = 'rateNreview'  # This sets the namespace 'rateNreview'

urlpatterns = [
    path('submit_rating/', submit_rating, name='submit_rating'),
    path('submit_review/', submit_review, name='submit_review'),
]
