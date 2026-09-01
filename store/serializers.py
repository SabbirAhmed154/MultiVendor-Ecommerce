from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    seller_name = serializers.CharField(
        source='seller.username',
        read_only=True
    )

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            'id',
            'seller',
            'seller_name',
            'category',
            'category_name',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'seller'
        ]