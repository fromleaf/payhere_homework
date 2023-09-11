from rest_framework.test import APITestCase

from payhere.utils import util_test


class BaseAccountTest(APITestCase):

    def setUp(self):
        self.TESTER_CELLPHONE = '01012341234'
        self.TESTER_PASSWORD = '123456'
        self.TESTER_NAME = '패이히어'
        util_test.signup(
            self.TESTER_CELLPHONE,
            self.TESTER_PASSWORD,
            self.TESTER_NAME,
        )
