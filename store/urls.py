from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOMEPAGE
    # =========================
    path(
        '',
        views.home,
        name='home'
    ),


    # =========================
    # PUBLIC SHOP
    # =========================
    path(
        'shop/',
        views.product_list,
        name='product_list'
    ),

    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),


    # =========================
    # PUBLIC SELLER STORE
    # =========================
    path(
        'store/<int:seller_id>/',
        views.seller_store,
        name='seller_store'
    ),


    # =========================
    # SELLER PRODUCTS
    # =========================
    path(
        'seller/products/',
        views.seller_product_list,
        name='seller_product_list'
    ),

    path(
        'seller/products/add/',
        views.product_add,
        name='product_add'
    ),

    path(
        'seller/products/<int:pk>/edit/',
        views.product_edit,
        name='product_edit'
    ),

    path(
        'seller/products/<int:pk>/delete/',
        views.product_delete,
        name='product_delete'
    ),

    path(
        'seller/products/<int:product_id>/images/add/',
        views.product_image_add,
        name='product_image_add'
    ),

    path(
        'seller/products/<int:product_id>/variants/add/',
        views.variant_add,
        name='variant_add'
    ),


    # =========================
    # CATEGORY
    # =========================
    path(
        'seller/categories/add/',
        views.category_add,
        name='category_add'
    ),


    # =========================
    # REVIEWS
    # =========================
    path(
        'product/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),

    path(
        'review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review'
    ),

    path(
        'review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review'
    ),
]