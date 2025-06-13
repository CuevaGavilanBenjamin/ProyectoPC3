from django.urls import path
from .views import DocumentoEmpresaAPIView, GenerarPDFAPIView,DocumentoDetailAPIView


urlpatterns = [
    path('empresa/', DocumentoEmpresaAPIView.as_view(), name='documentos_empresa_api'),
    path('empresa/<int:pk>/', DocumentoDetailAPIView.as_view(), name='documento_detalle_api'),
    path('generar-pdf/<int:pk>/', GenerarPDFAPIView.as_view(), name='generar_pdf_api'),
]