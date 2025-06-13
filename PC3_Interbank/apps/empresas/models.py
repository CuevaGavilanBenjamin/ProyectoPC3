from django.db import models


class Empresa(models.Model):
    razon_social   = models.CharField(max_length=255)
    ruc            = models.CharField(max_length=11, unique=True)
    representante  = models.CharField(max_length=255)
    correo         = models.EmailField(unique=True)
    password       = models.CharField(max_length=255)
    direccion      = models.CharField(max_length=255, blank=True, null=True)
    telefono       = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado         = models.CharField(max_length=20, default='pendiente')
    # Campos agregados para recomendaciones y benchmarking:
    sector         = models.CharField(max_length=100, blank=True, null=True)
    tamaño         = models.CharField(max_length=50, blank=True, null=True)
    antiguedad     = models.IntegerField(blank=True, null=True)  # años de antigüedad
    ubicacion      = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.razon_social} (RUC: {self.ruc})"

class Estrategia(models.Model):
    empresa= models.ForeignKey(Empresa,on_delete=models.CASCADE,related_name='estrategias')
    descripcion= models.TextField()
    fecha_registro= models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return f"{self.razon_social} (RUC: {self.ruc})"
    




class EstrategiaGeneral(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    sector = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50)
    antiguedad_min = models.IntegerField()
    antiguedad_max = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    etiquetas = models.CharField(max_length=200)  # Ejemplo: "marketing digital,crédito,alianzas"

    def __str__(self):
        return self.nombre

class PlanAccion(models.Model):
    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_limite = models.DateField()
    responsable = models.CharField(max_length=100)
    porcentaje_completado = models.FloatField(default=0)

    def __str__(self):
        return f"Plan para {self.empresa.razon_social} - {self.estrategia.nombre}"

class Tarea(models.Model):
    plan = models.ForeignKey(PlanAccion, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En proceso'), ('completada', 'Completada')], default='pendiente')
    fecha_limite = models.DateField(null=True, blank=True)
    responsable = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion} ({self.estado})"
