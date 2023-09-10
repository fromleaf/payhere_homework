import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from accounts.tests.base import BaseAccountTest


class TestSign(BaseAccountTest):
    def _is_verified_token(self, token):
        url = reverse('token_verify')
        data = {
            'token': token,
        }
        response = self.client.post(url, data, format='json')
        return response.status_code == status.HTTP_200_OK

    def _get_token(self, cellphone, password):
        url = reverse('token_obtain_pair')
        data = {
            'cellphone': cellphone,
            'password': password,
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            return

        token = json.loads(response.content.decode())
        return token

    def test_signup(self):
        url = reverse('signup')
        tester_cellphone = '01011112222'
        data = {
            'cellphone': tester_cellphone,
            'password': '1234',
            'name': 'Tester',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tester = User.objects.get(cellphone=tester_cellphone)
        self.assertEqual(tester.cellphone, tester_cellphone)

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'cellphone': self.TESTER_CELLPHONE,
            'password': self.TESTER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content.decode())
        is_verified_token = self._is_verified_token(token['access'])
        self.assertEqual(is_verified_token, True)

    def test_token_refresh(self):
        token = self._get_token(self.TESTER_CELLPHONE, self.TESTER_PASSWORD)

        url = reverse('token_refresh')
        data = {
            'refresh': token['refresh'],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_token = json.loads(response.content.decode())
        is_verified_token = self._is_verified_token(new_token['refresh'])
        self.assertEqual(is_verified_token, True)

    def test_logout(self):
        token = self._get_token(self.TESTER_CELLPHONE, self.TESTER_PASSWORD)

        url = reverse('logout')
        data = {
            'refresh': token['refresh'],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        is_verified_token = self._is_verified_token(token['refresh'])
        self.assertEqual(is_verified_token, False)
