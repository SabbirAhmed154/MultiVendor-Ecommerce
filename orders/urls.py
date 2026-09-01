from django.urls import path
from . import views

urlpatterns = [

    # CUSTOMER
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.order_history,
        name='order_history'
    ),

    path(
        'my-orders/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    # SELLER
    path(
        'seller/orders/',
        views.seller_order_list,
        name='seller_order_list'
    ),

    path(
        'seller/orders/item/<int:item_id>/status/',
        views.seller_update_order_status,
        name='seller_update_order_status'
    ),
]
