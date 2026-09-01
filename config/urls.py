from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
    'api/',
    include('store.api_urls')
),

    path(
        'admin/',
        admin.site.urls
    ),

    # Accounts
    path(
        '',
        include('accounts.urls')
    ),

    # Cart
    path(
        '',
        include('cart.urls')
    ),

    # Orders / Checkout
    path(
        '',
        include('orders.urls')
    ),

    # Store
    path(
        '',
        include('store.urls')
    ),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )