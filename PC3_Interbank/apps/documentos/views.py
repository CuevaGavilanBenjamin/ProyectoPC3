from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import Documento  # Ajusta el nombre del modelo si es diferente

@login_required(login_url='/login/')
@require_http_methods(["GET", "POST"])
def documentos_empresa(request):
    empresa = request.user.empresa
    if not empresa:
        return JsonResponse({'error': 'No tienes empresa asociada.'}, status=400)
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
    docs = Documento.objects.filter(empresa=empresa).values('id', 'nombre', 'archivo', 'fecha_subida')
    return JsonResponse(list(docs), safe=False)

def generar_pdf(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', 'Documento')
        contenido = request.POST.get('contenido', '')
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, nombre)
        p.drawString(100, 780, contenido)
        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="documento.pdf"'
        return response
    return HttpResponse("Método no permitido", status=405)
