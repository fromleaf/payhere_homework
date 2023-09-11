from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ErrorDetail
)

from payhere.constants import messages


class _BaseAPIException(APIException):
    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = ErrorDetail(detail, code)

    @property
    def error_data(self):
        params = {
            'code': self.default_code,
            'detail': self.default_detail
        }
        return params


class AlreadyRegisteredCellphone(_BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = messages.ALREADY_REGISTERED_CELLPHONE[0]
    default_detail = messages.ALREADY_REGISTERED_CELLPHONE[1]
