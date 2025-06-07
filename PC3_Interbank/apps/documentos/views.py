from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Documento  # Ajusta el nombre del modelo si es diferente

@login_required(login_url='/login/')
@require_http_methods(["GET", "POST"])
def documentos_empresa(request):
    empresa = request.user.empresa  # Ajusta si tu relación es diferente
    if request.method == "POST":
        archivo = request.FILES.get('archivo')
        nombre = request.POST.get('nombre')
        if archivo and nombre:
            doc = Documento.objects.create(
                empresa=empresa,
                nombre=nombre,
                archivo=archivo
            )
            return JsonResponse({'mensaje': 'Documento subido correctamente.'})
        return JsonResponse({'error': 'Faltan datos.'}, status=400)
    # GET: listar documentos
    docs = Documento.objects.filter(empresa=empresa).values('id', 'nombre', 'archivo', 'fecha_subida')
    return JsonResponse(list(docs), safe=False)
