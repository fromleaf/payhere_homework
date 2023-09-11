import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def signup(cellphone, password, name=None):
    client = APIClient()
    url = reverse('signup')
    data = {
        'cellphone': cellphone,
        'password': password,
    }

    if name:
        data['name'] = name

    response = client.post(url, data, format='json')
    if response.status_code != status.HTTP_201_CREATED:
        return

    content = json.loads(response.content.decode())
    return content


def get_token(cellphone, password):
    client = APIClient()

    url = reverse('token_obtain_pair')
    data = {
        'cellphone': cellphone,
        'password': password,
    }
    response = client.post(url, data, format='json')
    if response.status_code != status.HTTP_200_OK:
        return

    token = json.loads(response.content.decode())
    return token
