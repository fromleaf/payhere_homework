from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import User
from accounts.tests.base import BaseAccountTest
from payhere.constants import const
from payhere.utils import util_text
from products.models import Product


class BaseProductTest(APITestCase):
    def create_seller_product(self, cellphone, name):
        user = User.objects.get(cellphone=cellphone)

        data = {
            'seller': user,
            'category': "{} 상품 카테고리".format(name),
            'price': 1000,
            'cost': 800,
            'name': name,
            'description': "{} 상품 설명".format(name),
            'barcode': "1234-1234-{}".format(name),
            'expiration_date': timezone.now(),
            'size': const.PRODUCT_SIZE_SMALL,
        }

        created_product = Product.objects.create(**data)
        return created_product

    def create_seller_products(self, cellphone, count):
        user = User.objects.get(cellphone=cellphone)

        product_list = []
        for idx in range(count):
            data = {
                'seller': user,
                'category': "category {}".format(idx),
                'price': 1000 + idx,
                'cost': 800 + idx,
                'name': "상품 이름 {}".format(idx),
                'description': "상품 설명 {}".format(idx),
                'barcode': "1234-1234-{}".format(idx),
                'expiration_date': timezone.now(),
                'size': const.PRODUCT_SIZE_SMALL,
            }
            product_list.append(Product(**data))

        created_products = Product.objects.bulk_create(product_list)
        return created_products

    def setUp(self):
        self.TESTER_CELLPHONE = "01012341234"
        self.TESTER_PASSWORD = "123456"
        self.TESTER_NAME = "사장님"

        BaseAccountTest().create_user_by_signup_api(
            self.TESTER_CELLPHONE,
            self.TESTER_PASSWORD,
            self.TESTER_NAME,
        )

        self.create_seller_products(self.TESTER_CELLPHONE, 40)
        self.create_seller_product(self.TESTER_CELLPHONE, '슈크림 라떼')
