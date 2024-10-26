from django.urls import path
from .views import *

app_name = 'bookmark'

urlpatterns = [
    path('', bookmark_list, name='bookmark_list'),
    path('remove/<uuid:product_id>/', remove_bookmark, name='remove_bookmark'),
    path('toggle_bookmark/<int:product_id>/', toggle_bookmark, name='toggle_bookmark'),
    path('is_bookmarked/<uuid:product_id>/', is_bookmarked, name='is_bookmarked'),
]
