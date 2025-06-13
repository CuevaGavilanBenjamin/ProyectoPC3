from django.urls import path
from . import views

urlpatterns = [
   path('api/usuarios/', views.UsuarioListCreateAPIView.as_view(), name='usuarios_api'),
   path('api/usuarios/<int:pk>/', views.UsuarioRetrieveUpdateDestroyAPIView.as_view(), name='usuario_api'),
]