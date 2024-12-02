from django.urls import path
from authmobile.views import login, logout, register

app_name = 'authmobile'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),   
]