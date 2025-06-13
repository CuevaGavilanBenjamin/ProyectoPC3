from django.db import models
from apps.users.models import Usuario

class Documento(models.Model):
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tipo_documento = models.CharField(max_length=50, choices=[
        ('contrato', 'Contrato'),
        ('poder', 'Poder'),
        ('carta', 'Carta de presentación'),
        ('declaracion', 'Declaración jurada'),
        # ...otros tipos
    ], default='contrato')
    etiquetas = models.CharField(max_length=255, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    # ...otros campos si necesitas

    def __str__(self):
        return self.nombre
class Firma(models.Model):
    documento = models.ForeignKey('Documento', on_delete=models.CASCADE, related_name='firmas')
    firmante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('firmado', 'Firmado'), ('rechazado', 'Rechazado')], default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_firma = models.DateTimeField(null=True, blank=True)
    proveedor = models.CharField(max_length=50, blank=True, null=True)  # eSignatura.pe, Serpost, etc.
    hash_documento = models.CharField(max_length=128, blank=True, null=True)
    sello_tiempo = models.DateTimeField(null=True, blank=True)
    certificado = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)