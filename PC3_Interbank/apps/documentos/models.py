# apps/documentos/models.py

from django.db import models
from apps.empresas.models import Empresa

class Documento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
