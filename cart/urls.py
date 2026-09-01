from django.urls import path
from . import views


urlpatterns = [

    # CART
    path(
        'cart/',
        views.cart_detail,
        name='cart_detail'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/increase/<int:item_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:item_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),


    # COUPON
    path(
        'cart/apply-coupon/',
        views.apply_coupon,
        name='apply_coupon'
    ),

    path(
        'cart/remove-coupon/',
        views.remove_coupon,
        name='remove_coupon'
    ),


    # WISHLIST
    path(
        'wishlist/',
        views.wishlist_detail,
        name='wishlist_detail'
    ),

    path(
        'wishlist/add/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/remove/<int:item_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),

    path(
        'wishlist/to-cart/<int:item_id>/',
        views.wishlist_to_cart,
        name='wishlist_to_cart'
    ),

]