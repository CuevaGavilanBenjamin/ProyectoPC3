from rest_framework import serializers
from .models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['id', 'empresa', 'nombre', 'archivo', 'fecha_subida', 'tipo_documento', 'etiquetas', 'contenido']
        read_only_fields = ['empresa', 'fecha_subida']