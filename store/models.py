from django.db import models
from django.contrib.auth.models import User


# =========================
# CATEGORY MODEL
# =========================
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# =========================
# PRODUCT MODEL
# =========================
class Product(models.Model):

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    name = models.CharField(
        max_length=200,
        db_index=True
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
        default='',
        db_index=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            '-created_at'
        ]

        indexes = [

            # Active + category filtering
            models.Index(
                fields=[
                    'is_active',
                    'category'
                ],
                name='prod_active_cat_idx'
            ),

            # Active + brand filtering
            models.Index(
                fields=[
                    'is_active',
                    'brand'
                ],
                name='prod_active_brand_idx'
            ),

            # Active + price filtering
            models.Index(
                fields=[
                    'is_active',
                    'price'
                ],
                name='prod_active_price_idx'
            ),

            # Seller product filtering
            models.Index(
                fields=[
                    'seller',
                    'is_active'
                ],
                name='prod_seller_active_idx'
            ),

            # Latest active products
            models.Index(
                fields=[
                    'is_active',
                    'created_at'
                ],
                name='prod_active_date_idx'
            ),
        ]

    def __str__(self):
        return self.name


# =========================
# REVIEW MODEL
# =========================
class Review(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        db_index=True
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'product',
                    'user'
                ],
                name='unique_product_user_review'
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    'product',
                    'rating'
                ],
                name='review_prod_rating_idx'
            )
        ]

        ordering = [
            '-created_at'
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} - "
            f"{self.rating}"
        )


# =========================
# PRODUCT VARIANT MODEL
# =========================
class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    color = models.CharField(
        max_length=50,
        blank=True
    )

    size = models.CharField(
        max_length=20,
        blank=True
    )

    storage = models.CharField(
        max_length=50,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        indexes = [
            models.Index(
                fields=[
                    'product',
                    'color',
                    'size'
                ],
                name='variant_prod_cs_idx'
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.color} "
            f"{self.size} "
            f"{self.storage}"
        )


# =========================
# PRODUCT IMAGE MODEL
# =========================
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/gallery/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            '-created_at'
        ]

    def __str__(self):
        return f"{self.product.name} Image"