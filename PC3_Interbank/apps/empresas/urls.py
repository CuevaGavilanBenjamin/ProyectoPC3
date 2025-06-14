from django.urls import path
from .views import (
    home, registro_empresa, login_empresa, dashboard_empresa,estrategias_view,
    EmpresaRegistroView, EmpresaLoginView, PanelEmpresaView,PerfilEmpresaAPIView,SugerenciasEstrategiasView,BenchmarkingView,TareasPlanView,CompletarTareaView,ChecklistPDFView,
    perfil_empresa, eliminar_empresa, lista_empresas
)

urlpatterns = [
    path('', home, name='home'),
    path('registro-empresa/', registro_empresa, name='registro_empresa_form'),
    path('login/', login_empresa, name='login_empresa'),  # Solo para mostrar el HTML
    # API endpoints
    path('api/registro/', EmpresaRegistroView.as_view(), name='empresa_registro_api'),
    path('api/login/', EmpresaLoginView.as_view(), name='empresa_login_api'),
    path('api/panel-empresa/', PanelEmpresaView.as_view(), name='panel_empresa_api'),
    path('api/perfil/', PerfilEmpresaAPIView.as_view(), name='perfil_empresa_api'),
    # Admin/gestion
    path('admin/empresas/', lista_empresas, name='lista_empresas'),
    path('admin/empresas/eliminar/<int:empresa_id>/', eliminar_empresa, name='eliminar_empresa'),

    
    path('estrategias/', estrategias_view, name='estrategias_view'),
    path('estrategias/sugerencias/', SugerenciasEstrategiasView.as_view(), name='sugerencias_estrategias'),
    path('estrategias/benchmarking/', BenchmarkingView.as_view(), name='benchmarking_estrategias'),
    path('planes/<int:plan_id>/tareas/', TareasPlanView.as_view(), name='tareas_plan'),
    path('tareas/<int:tarea_id>/completar/', CompletarTareaView.as_view(), name='completar_tarea'),
    path('planes/checklist/pdf/', ChecklistPDFView.as_view(), name='checklist_pdf'),
]

