from django.urls import path
from ifnine_core.views import index, category_list_view, category_product_list_view, product_list_view, vendor_list_view

app_name = 'core'

urlpatterns=[
    # Homepage
    path('', index, name='index'),
    path('products/', product_list_view, name='product-list'),
    
    # category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    
    # vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
]