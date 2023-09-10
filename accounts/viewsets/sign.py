from rest_framework import (
    generics,
    status,
    views
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import SignupSerializer
from payhere.core.exceptions import AlreadyRegisteredCellphone
from payhere.core.permissions import AllowAny
from rest_framework.exceptions import ErrorDetail, ValidationError


class SignupViewSet(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except AlreadyRegisteredCellphone as e:
            return Response(e.error_data, status=e.status_code)

        return response


class LogoutViewSet(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
