from decimal import Decimal

from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save
from django.dispatch import receiver

from payhere.constants import const
from payhere.utils import util_text


class ProductQuerySet(QuerySet):
    def exclude_deleted_products(self):
        queryset = self.filter(deleted_at__isnull=True)
        return queryset

    def by_seller(self, seller_id, exclude_deleted_products=True):
        if exclude_deleted_products:
            queryset = self.exclude_deleted_products()
        else:
            queryset = self

        queryset = queryset.filter(seller=seller_id)
        return queryset


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Product(models.Model):
    PRODUCT_SIZE_CHOICES = {
        (const.PRODUCT_SIZE_SMALL, const.PRODUCT_SIZE_SMALL),
        (const.PRODUCT_SIZE_LARGE, const.PRODUCT_SIZE_LARGE),
    }

    objects = ProductManager.from_queryset(ProductQuerySet)()

    seller = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        help_text="상품 등록자"
    )
    category = models.CharField(
        max_length=const.MAX_LENGTH_DEFAULT_CHAR,
        help_text="카테고리"
    )
    price = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        default=Decimal(0),
        help_text="가격"
    )
    cost = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        default=Decimal(0),
        help_text="원가"
    )
    name = models.CharField(
        max_length=const.MAX_LENGTH_NAME,
        help_text="이름"
    )
    name_to_choseong = models.CharField(
        null=True,
        blank=True,
        default='',
        max_length=512,
        help_text="이름(초성 검색을 위해서 상품 이름에서 초성만 저장)"
    )
    description = models.CharField(
        max_length=const.MAX_LENGTH_DESC,
        help_text="설명"
    )
    barcode = models.CharField(
        max_length=const.MAX_LENGTH_DEFAULT_CHAR,
        help_text="바코드"
    )
    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        help_text="유통기한"
    )
    size = models.CharField(
        choices=sorted(PRODUCT_SIZE_CHOICES),
        default=const.PRODUCT_SIZE_SMALL,
        max_length=const.MAX_LENGTH_DEFAULT_CHAR,
        help_text="사이즈"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        help_text="상품 삭제일(날짜값이 있으면, 삭제된 상태임)"
    )

    @property
    def is_deleted(self):
        return self.deleted_at is not None


@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, raw, using, update_fields, **kwargs):
    instance.name_to_choseong = util_text.get_choseong(instance.name)
