from django.urls import path, include
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('preferences/', include('preference.urls')),
]