# core/urls.py
from django.urls import path
from .views import index, search, order_detail, leave_review, wishlist_detail, add_to_wishlist,remove_from_wishlist,  cart_detail, add_to_cart,update_cart_item,  product_list, product_detail, add_product, cart, checkout, order_history, register

urlpatterns = [
    path('', index, name='home-url'), 
    path('product_list/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-product/', add_product, name='add_product'),
    # path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-history/', order_history, name='order_history'),
    path('register/', register, name='register'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist_detail, name='wishlist_detail'),
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('product/<int:product_id>/review/', leave_review, name='leave_review'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),

    path('search/', search, name='search'),

    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
