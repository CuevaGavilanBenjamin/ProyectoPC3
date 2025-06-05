# apps/documentos/models.py

from django.db import models
from apps.empresas.models import Empresa

class Documento(models.Model):
    TIPO_CHOICES = [
        ('contrato', 'Contrato'),
        ('poder', 'Poder'),
        ('declaracion', 'Declaración'),
        # etc. según necesites
    ]

    empresa     = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    tipo        = models.CharField(max_length=50, choices=TIPO_CHOICES)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado      = models.CharField(max_length=20, default='pendiente')
    ruta        = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.id} de {self.empresa.razon_social}"
