from django.urls import path
from bookmark.views import*

app_name = 'bookmark'

urlpatterns = [
    path('', bookmark_list, name='bookmark_list'),
    path('remove/<uuid:product_id>/', remove_bookmark, name='remove_bookmark'),
    path('toggle_bookmark/<uuid:product_id>/', toggle_bookmark, name='toggle_bookmark'),
<<<<<<< HEAD
    path('save_note/<uuid:product_id>/', save_note, name='save_note'),
=======
    path('add_or_edit_note/', add_or_edit_note, name='add_or_edit_note'),
>>>>>>> 57768dc6b095887ba0b8374981a2151ad660f53a
]