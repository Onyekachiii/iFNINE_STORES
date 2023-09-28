from django.urls import path, include
from ifnine_core.views import index, category_list_view, category_product_list_view, product_list_view, vendor_list_view, vendor_detail_view, product_detail_view, tag_list, ajax_add_review, search_view, filter_product, add_to_cart, cart_view, delete_item_from_cart, update_cart, checkout_view, payment_completed_view, payment_failed_view, customer_dashboard, user_history, order_detail, make_address_default, add_to_wishlist, wishlist_view, contact, ajax_contact_form, remove_from_wishlist

app_name = 'core'

urlpatterns=[
    # Homepage
    path('', index, name='index'),
    path('products/', product_list_view, name='product-list'),
    path('products/<pid>/', product_detail_view, name='product-detail'),
    
    
    # category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    
    # vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    
    # Tags
    path('products/tag/<slug:tag_slug>/', tag_list, name='tags'),
    
    # Reviews
    path('ajax-add-review/<int:pid>/', ajax_add_review, name='ajax-add-review'),
    
    # Search
    path('search/', search_view, name='search'),
    
    # Filter product URL
    path('filter-products/', filter_product, name='filter-product'),
    
    #Add to cart URL
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    
    # Cart page URL
    path('cart/', cart_view, name='cart'),
    
    # Delete item from cart
    path('delete-from-cart/', delete_item_from_cart, name='delete-from-cart'),
    
    # Update items in cart
    path('update-cart/', update_cart, name='update-cart'),
    
    # checkout url
    path('checkout/', checkout_view, name='checkout'),
    
    # Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    # Payment succesful
    path('payment-completed/', payment_completed_view, name='payment-completed'),
    
    # checkout url
    path('payment-failed/', payment_failed_view, name='payment-failed'),
    
    # User Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'),
    
    # User History
    path('user-history/', user_history, name='user-history'),
    
    # Order detail
    path('user-history/order/<int:id>', order_detail, name='order-detail'),
    
    # Making address default
    path('make-default-address', make_address_default, name='make-default-address'),
    
     # Wishlist page URL
    path('wishlist/', wishlist_view, name='wishlist'),
    
    # Adding to wishlist
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    
    # Deleting from wishlist
    path('remove-from-wishlist/', remove_from_wishlist, name='remove-from-wishlist'),
    
    # Making address default
    path('contact/', contact, name='contact'),
    path('ajax-contact-form/', ajax_contact_form, name='ajax-contact-form'),
]