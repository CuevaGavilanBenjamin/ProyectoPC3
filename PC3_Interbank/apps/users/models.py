# apps/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.empresas.models import Empresa

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'superadmin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('empresa', 'Empresa'),
        ('mentor', 'Mentor'),
        ('superadmin', 'Superadmin'),
    ]

    empresa       = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='usuarios',
        blank=True,
        null=True
    )
    nombre        = models.CharField(max_length=255)
    dni           = models.CharField(max_length=8, unique=True, blank=True, null=True)
    correo        = models.EmailField(unique=True)
    rol           = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Campos obligatorios para AbstractBaseUser
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'rol']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} ({self.correo})"
