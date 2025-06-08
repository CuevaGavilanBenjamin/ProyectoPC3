from django.urls import path
from .views import documentos_empresa, generar_pdf

urlpatterns = [
    path('empresa/', documentos_empresa, name='documentos_empresa'),
    path('generar-pdf/', generar_pdf, name='generar_pdf'),
]