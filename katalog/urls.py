from django.urls import path, include
from katalog.views import *

app_name = 'katalog'

urlpatterns = [
    path('', show_katalog, name = 'show_katalog'),
]