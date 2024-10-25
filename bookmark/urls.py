from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('add/<int:product_id>/', views.add_bookmark, name='add_bookmark'),
    path('remove/<int:product_id>/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmark_list/', views.bookmark_list, name='bookmark_list'),
]