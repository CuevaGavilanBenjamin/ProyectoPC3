from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import Documento
from .serializers import DocumentoSerializer

# Listar y crear documentos
class DocumentoEmpresaAPIView(generics.ListCreateAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Documento.objects.filter(empresa=self.request.user.empresa)

    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)

# Recuperar, actualizar y eliminar un documento específico
class DocumentoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Documento.objects.filter(empresa=self.request.user.empresa)

class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'

    def render(self, data, media_type=None, renderer_context=None):
        return data
# Generar PDF de un documento específico
class GenerarPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [PDFRenderer]

    def get(self, request, pk):
        doc = Documento.objects.filter(pk=pk, empresa=request.user.empresa).first()
        if not doc:
            return HttpResponse("Documento no encontrado", status=404)
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, doc.nombre)
        p.drawString(100, 780, doc.contenido or '')
        p.showPage()
        p.save()
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{doc.nombre}.pdf"'
        return response