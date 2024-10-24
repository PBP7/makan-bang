from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('bookmarks/', views.bookmarked_products, name='bookmarked_products'),
    path('toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
]