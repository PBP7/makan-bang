# preference/urls.py
from django.urls import path
from . import views

app_name = 'preference'

urlpatterns = [
    path('preferences/', views.show_preference, name='show_preference'),
    path('', views.preference_page,name='add_preference'),
    path('create-ajax/', views.add_preference_ajax, name='add_ajax'),
    path('delete-ajax/<uuid:preference_id>/', views.delete_preference_ajax, name='delete_ajax'),
    path('get-preferences/', views.get_preferences, name='get_preferences'),
]