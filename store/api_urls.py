from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet


router = DefaultRouter()

router.register(
    'products',
    ProductViewSet,
    basename='api-products'
)

urlpatterns = router.urls