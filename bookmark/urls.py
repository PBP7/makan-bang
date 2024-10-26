from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('bookmarks/remove/<int:product_id>/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmarks/button/<int:product_id>/', views.toggle_bookmark, name='toggle_bookmark'),
]