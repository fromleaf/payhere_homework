from django.urls import reverse
from rest_framework.test import APITestCase


class BaseAccountTest(APITestCase):

    def create_user_by_signup_api(self, cellphone, password, name=None):
        url = reverse('signup')
        data = {
            'cellphone': cellphone,
            'password': password,
        }

        if name:
            data['name'] = name

        response = self.client.post(url, data, format='json')
        return response

    def setUp(self):
        self.TESTER_CELLPHONE = '01012341234'
        self.TESTER_PASSWORD = '123456'
        self.TESTER_NAME = '패이히어'
        self.TESTER = self.create_user_by_signup_api(
            self.TESTER_CELLPHONE,
            self.TESTER_PASSWORD,
            self.TESTER_NAME,
        )
