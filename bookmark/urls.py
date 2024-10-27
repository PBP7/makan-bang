from django.urls import path
from bookmark.views import*

app_name = 'bookmark'

urlpatterns = [
    path('', bookmark_list, name='bookmark_list'),
    path('remove/<uuid:product_id>/', remove_bookmark, name='remove_bookmark'),
    path('toggle_bookmark/<uuid:product_id>/', toggle_bookmark, name='toggle_bookmark'),
]