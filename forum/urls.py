from django.urls import path, include
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name = 'show_forum'),
    path('create-new-forum', create_new_forum, name='create_new_forum'),
    path('edit-forum/<int:id>', edit_forum, name='edit_forum'),
    path('delete-forum/<int:id>', delete_forum, name='delete_forum'),
    path('view-forum/<int:id>', view_forum, name='view_forum'),
    path('public-forum/', public_forum, name='public_forum'),
    path('your-posts/', your_posts, name='your_posts'),
    path('filter-by-topic/', public_forum, name='filter_by_topic'),
    path('new-forum-ajax', new_forum_ajax, name='new_forum_ajax'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]