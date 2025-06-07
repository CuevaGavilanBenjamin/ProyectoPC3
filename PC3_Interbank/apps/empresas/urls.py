from django.urls import path
from .views import registro_empresa, EmpresaRegistroView, home

urlpatterns = [
    path('', home, name='home'),
    path('registro-empresa/', registro_empresa, name='registro_empresa_form'),
    path('registro/', EmpresaRegistroView.as_view(), name='empresa_registro'),
]