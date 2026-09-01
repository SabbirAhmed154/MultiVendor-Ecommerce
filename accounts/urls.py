from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path(
        'register/customer/',
        views.customer_register,
        name='customer_register'
    ),

    path(
        'register/seller/',
        views.seller_register,
        name='seller_register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'dashboard/',
        views.role_dashboard,
        name='role_dashboard'
    ),

    path(
        'customer/dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    path(
        'seller/dashboard/',
        views.seller_dashboard,
        name='seller_dashboard'
    ),
]