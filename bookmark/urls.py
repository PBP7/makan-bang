from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('bookmarks/remove/<int:product_id>/', views.remove_bookmark, name='remove_bookmark'),

]