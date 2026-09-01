from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .models import Product
from .serializers import ProductSerializer
from accounts.models import Profile


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        # Everyone can see active products
        if self.action in ['list', 'retrieve']:
            return Product.objects.filter(
                is_active=True
            ).order_by('-created_at')

        # Seller can edit/delete only own products
        if self.request.user.is_authenticated:
            return Product.objects.filter(
                seller=self.request.user
            )

        return Product.objects.none()

    def perform_create(self, serializer):

        is_seller = Profile.objects.filter(
            user=self.request.user,
            role='seller'
        ).exists()

        if not is_seller:
            raise PermissionDenied(
                "Only sellers can create products."
            )

        serializer.save(
            seller=self.request.user
        )