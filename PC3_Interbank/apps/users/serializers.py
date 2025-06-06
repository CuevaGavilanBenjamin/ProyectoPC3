# tu_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nombre'] = user.nombre
        token['rol'] = user.rol
        if user.empresa:
            token['empresa_id'] = user.empresa.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['nombre'] = self.user.nombre
        data['rol'] = self.user.rol
        return data
