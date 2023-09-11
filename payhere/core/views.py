from rest_framework import views

from payhere.utils import util_api


class BaseAPIView(views.APIView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response = util_api.reform_response(self, response)
        return response
