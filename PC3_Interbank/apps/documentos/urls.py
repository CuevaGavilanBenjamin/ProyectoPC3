from django.urls import path
from .views import documentos_empresa

urlpatterns = [
    path('empresa/', documentos_empresa, name='documentos_empresa'),
]