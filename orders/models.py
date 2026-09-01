from django.db import models
from django.contrib.auth.models import User

from store.models import Product, ProductVariant


# ==========================================
# ORDER
# ==========================================
class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id}"


# ==========================================
# ORDER ITEM
# ==========================================
class OrderItem(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )

    variant_color = models.CharField(
        max_length=50,
        blank=True
    )

    variant_size = models.CharField(
        max_length=20,
        blank=True
    )

    variant_storage = models.CharField(
        max_length=50,
        blank=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):

        variant_text = ""

        if self.variant_color:
            variant_text += f" {self.variant_color}"

        if self.variant_size:
            variant_text += f" {self.variant_size}"

        if self.variant_storage:
            variant_text += f" {self.variant_storage}"

        return (
            f"{self.product.name}"
            f"{variant_text} x {self.quantity}"
        )


# ==========================================
# COUPON
# ==========================================
class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percent = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.code} - "
            f"{self.discount_percent}%"
        )