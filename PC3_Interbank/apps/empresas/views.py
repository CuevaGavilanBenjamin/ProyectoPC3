from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import EmpresaRegistroSerializer

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

def home(request):
    return render(request, 'index.html')

def registro_empresa(request):
    return render(request, 'registro_empresa.html')

 