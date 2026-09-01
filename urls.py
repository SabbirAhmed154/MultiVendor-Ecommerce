urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('store.urls')),
]
