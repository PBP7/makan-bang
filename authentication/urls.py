from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('register/', register, name='register'),
    path('login-mobile/', login_mobile, name='login-mobile'),
    path('logout-mobile/', logout_mobile, name='logout-mobile'),
    path('register-mobile/', register_mobile, name='register-mobile'),   
]