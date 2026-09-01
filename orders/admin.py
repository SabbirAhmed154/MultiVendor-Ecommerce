from django.contrib import admin
from .models import Order, OrderItem, Coupon


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'payment_method',
        'status',
        'created_at',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
        'status',
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_percent',
        'is_active',
        'created_at',
    )

    search_fields = (
        'code',
    )

    list_filter = (
        'is_active',
    )