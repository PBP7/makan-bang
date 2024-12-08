# preference/urls.py
from django.urls import path
from . import views

app_name = 'preference'

urlpatterns = [
    path('', views.preference_page, name='show_preference'),
    path('add/', views.show_preference, name='show_preference'),
    path('create-ajax/', views.add_preference_ajax, name='add_ajax'),
    path('delete-ajax/<int:preference_id>/', views.delete_preference_ajax, name='delete_ajax'),
    path('get-preferences/', views.get_preferences, name='get_preferences'),
    path('get-products/', views.get_products, name='get_products'),
    path('get-matching-products/', views.get_matching_products, name='get_matching_products'),
    path('get-user-preferences-json/', views.get_user_preferences_json, name='get_user_preferences_json'),
]
