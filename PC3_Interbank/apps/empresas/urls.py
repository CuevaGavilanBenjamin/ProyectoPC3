from django.urls import path
from .views import registro_empresa, EmpresaRegistroView, home, eliminar_empresa, lista_empresas, EmpresaLoginView, login_empresa, dashboard_empresa, perfil_empresa

from .views import (
    home, registro_empresa, login_empresa, dashboard_empresa,
    EmpresaRegistroView, EmpresaLoginView, PanelEmpresaView,PerfilEmpresaAPIView,
    perfil_empresa, eliminar_empresa, lista_empresas
)

urlpatterns = [
    path('', home, name='home'),
    path('registro-empresa/', registro_empresa, name='registro_empresa_form'),
    path('login/', login_empresa, name='login_empresa'),  # Solo para mostrar el HTML
    path('dashboard/', dashboard_empresa, name='dashboard_empresa'),  # Solo para mostrar el HTML
    # API endpoints
    path('api/registro/', EmpresaRegistroView.as_view(), name='empresa_registro_api'),
    path('api/login/', EmpresaLoginView.as_view(), name='empresa_login_api'),
    path('api/panel-empresa/', PanelEmpresaView.as_view(), name='panel_empresa_api'),
    path('api/perfil/', PerfilEmpresaAPIView.as_view(), name='perfil_empresa_api'),
    # Admin/gestion
    path('admin/empresas/', lista_empresas, name='lista_empresas'),
    path('admin/empresas/eliminar/<int:empresa_id>/', eliminar_empresa, name='eliminar_empresa'),
]