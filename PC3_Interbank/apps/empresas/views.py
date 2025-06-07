from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .serializers import EmpresaRegistroSerializer
from .models import Empresa

class PanelEmpresaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.rol != 'empresa':
            return Response({'error': 'Acceso no autorizado'}, status=403)

        return Response({
            "mensaje": f"Hola {request.user.nombre}, bienvenido al panel de empresa.",
            "rol": request.user.rol
        })

class EmpresaRegistroView(APIView):
    permission_classes = []  # Público

    def post(self, request):
        serializer = EmpresaRegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Empresa registrada correctamente.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpresaLoginView(APIView):
    permission_classes = []

    def post(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')
        try:
            empresa = Empresa.objects.get(correo=correo)
            print("Contraseña enviada:", password)
            print("Contraseña en BD:", empresa.password)
            print("Check:", check_password(password, empresa.password))
            if empresa.estado != 'activo':
                return Response({'error': 'Tu empresa aún no está activa.'}, status=403)
            if check_password(password, empresa.password):
                return Response({'mensaje': 'Login exitoso.'})
            else:
                return Response({'error': 'Contraseña incorrecta.'}, status=400)
        except Empresa.DoesNotExist:
            return Response({'error': 'Correo no registrado.'}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def eliminar_empresa(request, empresa_id):
    try:
        empresa = Empresa.objects.get(id=empresa_id)
        empresa.delete()
        return Response({'mensaje': 'Empresa eliminada correctamente.'})
    except Empresa.DoesNotExist:
        return Response({'error': 'Empresa no encontrada.'}, status=404)

@staff_member_required
def lista_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'lista_empresas.html', {'empresas': empresas})

@staff_member_required
def eliminar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.delete()
    return redirect('lista_empresas')

def home(request):
    return render(request, 'index.html')

def registro_empresa(request):
    return render(request, 'registro_empresa.html')

def login_empresa(request):
    return render(request, 'login.html')

@login_required(login_url='/login/')
def dashboard_empresa(request):
    # Aquí puedes pasar datos de la empresa si lo deseas
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
@require_http_methods(["GET", "POST"])
def perfil_empresa(request):
    empresa = Empresa.objects.filter(correo=request.user.correo).first()
    if request.method == "POST":
        data = request.POST
        empresa.razon_social = data.get('razon_social', empresa.razon_social)
        empresa.representante = data.get('representante', empresa.representante)
        empresa.direccion = data.get('direccion', empresa.direccion)
        empresa.telefono = data.get('telefono', empresa.telefono)
        empresa.save()
        return JsonResponse({'mensaje': 'Perfil actualizado correctamente.'})
    # Para GET, devuelve los datos de la empresa
    return JsonResponse({
        'razon_social': empresa.razon_social,
        'ruc': empresa.ruc,
        'representante': empresa.representante,
        'correo': empresa.correo,
        'direccion': empresa.direccion,
        'telefono': empresa.telefono,
    })

