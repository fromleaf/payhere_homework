from django.db import IntegrityError
from rest_framework import serializers

from accounts.models import User
from payhere.core.exceptions import AlreadyRegisteredCellphone


class SignupSerializer(serializers.ModelSerializer):
    cellphone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'cellphone',
            'password',
            'name'
        ]
        read_only_fields = [
            'id'
        ]

    def save(self, **kwargs):
        try:
            instance = self.create(self.validated_data)
        except IntegrityError:
            raise AlreadyRegisteredCellphone

        instance.set_password(self.validated_data.get('password'))
        instance.save()
        return instance
