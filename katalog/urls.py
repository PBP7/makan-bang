from django.urls import path, include
from katalog.views import *


app_name = 'katalog'

urlpatterns = [
    path('', show_katalog, name = 'show_katalog'),
    path('create-product-entry-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('delete/<uuid:id>', delete_product_entry, name='delete_product_entry'),
    path('edit/<uuid:id>', edit_product_entry, name='edit_product_entry'),

]