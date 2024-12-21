from django.urls import path
from bookmark.views import*

app_name = 'bookmark'

urlpatterns = [
    path('', bookmark_list, name='bookmark_list'),
    path('remove/<uuid:product_id>/', remove_bookmark, name='remove_bookmark'),
    path('toggle_bookmark/<uuid:product_id>/', toggle_bookmark, name='toggle_bookmark'),
    path('add_or_edit_note/', add_or_edit_note, name='add_or_edit_note'),
    path('add-bookmark-flutter/', add_bookmark_flutter, name='add_bookmark_flutter'),
    path('delete-bookmark-flutter/<uuid:product_id>/', delete_bookmark_flutter, name='delete_bookmark_flutter'),
    path('toggle-bookmark-flutter/<uuid:product_id>/',toggle_bookmark_flutter, name='toggle_bookmark_flutter'),
    path('bookmarked-list/',bookmarked_list, name='bookmarked_list'),


]