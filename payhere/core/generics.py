from rest_framework import generics

from payhere.utils import util_api


class BaseCreateAPIView(generics.CreateAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response = util_api.reform_response(self, response)
        return response
