# apps/empresas/serializers.py

from rest_framework import serializers
from .models import Empresa
import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id',
            'razon_social',
            'ruc',
            'representante',
            'correo',
            'direccion',
            'telefono',
            'fecha_registro',
            'estado',
        ]
        read_only_fields = ['id', 'fecha_registro', 'estado']
    def validate_ruc(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("El RUC debe tener 11 dígitos numéricos.")
        return value

class EmpresaRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Empresa
        fields = ['razon_social', 'ruc', 'representante', 'correo', 'password', 'direccion', 'telefono']

    def validate_correo(self, value):
        if Empresa.objects.filter(correo=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        # Validación de formato de correo
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Formato de correo inválido.")
        return value

    def validate_ruc(self, value):
        if Empresa.objects.filter(ruc=value).exists():
            raise serializers.ValidationError("Este RUC ya está registrado.")
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("El RUC debe tener exactamente 11 dígitos numéricos.")
        return value

    def create(self, validated_data):
        # Hashea la contraseña antes de guardar
        password = validated_data.pop('password')
        empresa = Empresa(**validated_data)
        empresa.password = make_password(password)
        empresa.save()

        # Envío de correo de confirmación (opcional)
        send_mail(
            subject='Registro exitoso en PC3',
            message=f'Hola {empresa.representante}, tu empresa ha sido registrada exitosamente en PC3.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[empresa.correo],
            fail_silently=True,
        )
        return empresa