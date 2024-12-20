from django.urls import path
from rate_review.views import submit_review, product_detail, show_json, show_json_by_id, show_xml, show_xml_by_id
from rate_review.views import create_review_flutter, delete_review_flutter, edit_review_flutter, show_review_flutter    
from rate_review import views

app_name = 'rate_review'

urlpatterns = [
    #('rate_review/<uuid:id>/', product_detail, name='rate_review'),
    path('submit_review/<uuid:id>/', submit_review, name='submit_review'),
    path('product_detail/<uuid:id>/', views.product_detail, name='product_detail'),
    path('delete_review/<uuid:review_id>/', views.delete_review, name='delete_review'),
    path('edit_review/<uuid:review_id>/', views.edit_review, name='edit_review'),

    path('user_rating/', views.user_rating, name='user_rating'),

    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    
    path('create-flutter/', create_review_flutter, name='create_review_flutter'),
    path('delete-flutter/<uuid:id>', delete_review_flutter, name='delete_review_flutter'),
    path('edit-flutter/<uuid:id>', edit_review_flutter, name='edit_review_flutter'),
    path('show-flutter/<uuid:id>', show_review_flutter, name='show_review_flutter'),
]

