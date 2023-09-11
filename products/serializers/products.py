
from rest_framework import serializers

from payhere.utils import util_text
from products.models import Product


class SellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CreateOrUpdateSellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'price',
            'cost',
            'name',
            'name_to_choseong',
            'description',
            'barcode',
            'expiration_date',
            'size',
        ]
        read_only_fields = [
            'id',
            'name_to_choseong',
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['seller'] = self.context['request'].user
        return ret
