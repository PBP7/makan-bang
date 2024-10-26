from django.urls import path
from rateNreview.views import *
app_name = 'rateNreview'  # This sets the namespace 'rateNreview'

urlpatterns = [
    path('', show_rateNreview, name='show_rateNreview'),
    path('add-review/', add_review, name='add_review'),
    path('edit_review/<uuid:product_id>/', edit_review, name='edit_review'),
    path('delete-review/<uuid:product_id>', delete_review, name='delete_review'),
    path('review/<uuid:product_id>/reviews/', product_reviews, name='product_reviews'),
    path('product/<uuid:product_id>/reviews', product_reviews, name='product_reviews'),




]
