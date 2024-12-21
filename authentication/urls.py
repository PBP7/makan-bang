from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('register/', register, name='register'),
    path('login-mobile/', login, name='login-mobile'),
    path('logout-mobile/', logout, name='logout-mobile'),
    path('register-mobile/', register_mobile, name='register-mobile'),   
]