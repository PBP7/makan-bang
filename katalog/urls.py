from django.urls import path, include
from katalog.views import *


app_name = 'katalog'

urlpatterns = [
    path('', show_katalog, name='show_katalog'),
    path('create-product-entry-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('delete/<uuid:id>', delete_product_entry, name='delete_product_entry'),
    path('edit/<uuid:id>', edit_product_entry, name='edit_product_entry'),
    path('preference/', include ('preference.urls')),
    path('dataset', dataset, name='dataset'),
    path('edit/', edit, name='edit'),
    path('delete/', edit, name='delete'),
    path('search/', search_products, name='search_products'),
    path('reimport/', reimport_dataset, name='reimport_dataset'),
    path('get_all_products/', get_all_products, name='get_all_products'),
    path('rate_review/', include ('rate_review.urls')),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]