from django.urls import (
    include,
    path
)
from rest_framework import routers

from products.viewsets.products import SellerProductViewSet

routers = routers.DefaultRouter()
routers.register(
    'seller',
    SellerProductViewSet,
    basename='seller-products'
)

urlpatterns = [
    path('', include(routers.urls)),
]
