import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from payhere.constants import const
from payhere.utils import util_test
from products.models import Product
from products.tests.base import BaseProductTest


class ProductTest(BaseProductTest):
    def _get_client(self):
        token = util_test.get_token(
            self.TESTER_CELLPHONE,
            self.TESTER_PASSWORD
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])
        return client

    def test_get_products(self):
        client = self._get_client()

        url = reverse('seller-products-list')
        response = client.get(url)
        content = json.loads(response.content.decode())

        # HTTP status 확인 및 요청한 products data 및 next cursor 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(content)
        self.assertIsNotNone(content['data']['next'])

    def test_create_products(self):
        client = self._get_client()

        url = reverse('seller-products-list')
        data = {
            'category': "카테고리",
            'price': "30000",
            'cost': "28000",
            'name': "상품 이름",
            'description': "상품 설명",
            'barcode': "111122223333",
            'expiration_date': timezone.now(),
            'size': const.PRODUCT_SIZE_LARGE,
        }
        response = client.post(url, data=data, format='json')
        content = json.loads(response.content.decode())

        # 생성됐다는 HTTP status 확인 및 생성된 product 정보 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(content)

        created_product_id = content['data']['id']
        is_exists = Product.objects.filter(id=created_product_id).exists()
        self.assertEqual(is_exists, True)

    def test_update_products(self):
        seller = User.objects.get(cellphone=self.TESTER_CELLPHONE)
        before_update_product = Product.objects.by_seller(seller.id).first()

        client = self._get_client()
        url = reverse(
            'seller-products-detail',
            args=[before_update_product.id]
        )
        data = {
            'category': "카테고리 수정",
            'price': "60000",
            'cost': "38000",
            'name': "상품 이름 수정",
        }
        response = client.patch(url, data=data, format='json')
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(content)

        # 업데이트 전 product 정보와 업데이트 완료 후 product 정보 비교
        updated_product_id = content['data']['id']
        after_update_product = Product.objects.get(id=updated_product_id)
        self.assertNotEquals(before_update_product.category, after_update_product.category)
        self.assertNotEquals(before_update_product.price, after_update_product.price)
        self.assertNotEquals(before_update_product.cost, after_update_product.cost)
        self.assertNotEquals(before_update_product.name, after_update_product.name)

    def test_delete_products(self):
        seller = User.objects.get(cellphone=self.TESTER_CELLPHONE)
        product = Product.objects.by_seller(seller.id).first()

        client = self._get_client()
        url = reverse(
            'seller-products-detail',
            args=[product.id]
        )

        # 삭제됐다는 HTTP status 확인
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 삭제된 product의 deleted_at와 is_deleted 값 확인
        deleted_product = Product.objects.get(id=product.id)
        self.assertIsNotNone(deleted_product.deleted_at)
        self.assertEqual(deleted_product.is_deleted, True)

    def test_search_by_product_name(self):
        client = self._get_client()

        def search_by_keyword(string):
            url = reverse('seller-products-list')
            url = '{}?search={}'.format(url, string)
            response = client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            content = json.loads(response.content.decode())
            self.assertIsNotNone(content)
            return content

        # 각각의 단어 및 초성 검색 결과 확인
        result = search_by_keyword('슈크림')
        self.assertNotEqual(result['data']['results'], [])

        result = search_by_keyword('크림')
        self.assertNotEqual(result['data']['results'], [])

        result = search_by_keyword('라떼')
        self.assertNotEqual(result['data']['results'], [])

        result = search_by_keyword('ㅅㅋㄹ')
        self.assertNotEqual(result['data']['results'], [])

        result = search_by_keyword('ㄹㄸ')
        self.assertNotEqual(result['data']['results'], [])
