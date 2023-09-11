from django.utils import timezone
from rest_framework import filters

from payhere.core.pagination import SellerProductCursorPagination
from payhere.core.permissions import IsAuthenticated
from payhere.core.viewsets import BaseModelViewSet
from products.models import Product
from products.serializers.products import (
    CreateOrUpdateSellerProductSerializer,
    SellerProductSerializer
)


class SellerProductViewSet(BaseModelViewSet):
    serializer_class = SellerProductSerializer
    create_or_update_serializer_class = CreateOrUpdateSellerProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    pagination_class = SellerProductCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_to_choseong']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return self.create_or_update_serializer_class
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.by_seller(self.request.user.id)
        queryset = queryset.order_by('-id')
        return queryset

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
