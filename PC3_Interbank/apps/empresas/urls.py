from django.urls import path
from .views import registro_empresa, EmpresaRegistroView, home, eliminar_empresa, lista_empresas, EmpresaLoginView, login_empresa, dashboard_empresa, perfil_empresa

urlpatterns = [
    path('', home, name='home'),
    path('registro-empresa/', registro_empresa, name='registro_empresa_form'),
    path('registro/', EmpresaRegistroView.as_view(), name='empresa_registro'),
    path('eliminar/<int:empresa_id>/', eliminar_empresa, name='eliminar_empresa'),
    path('admin/empresas/', lista_empresas, name='lista_empresas'),
    path('admin/empresas/eliminar/<int:empresa_id>/', eliminar_empresa, name='eliminar_empresa'),
    path('login/', login_empresa, name='login_empresa'),  # HTML (formulario)
    path('api/login/', EmpresaLoginView.as_view(), name='empresa_login_api'),  # API (POST)
    path('dashboard/', dashboard_empresa, name='dashboard_empresa'),
    path('perfil/', perfil_empresa, name='perfil_empresa'),
]