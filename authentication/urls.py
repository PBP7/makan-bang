from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('register/', register, name='register'),
    path('login_mobile/', login_mobile, name='login_mobile'),  # untuk mobile
    path('register_mobile/', register_mobile, name='register_mobile'),  # untuk mobile
    path('logout_mobile/', logout_mobile, name='logout_mobile'),
]