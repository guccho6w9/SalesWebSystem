from django.db import models
from django.utils import timezone

# Create your models here.

class Producto(models.Model):
    id_pd = models.AutoField(primary_key=True)
    cod = models.CharField(max_length=20)
    des = models.CharField(max_length=75, blank=False)
    pre = models.FloatField(blank=False)
    aju = models.CharField(max_length=4, blank=False)
    ofe = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return f"{self.cod} {self.des} {self.pre} {self.aju} {self.ofe}"
    

    

class HistorialProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_anterior = models.CharField(max_length=255)
    cod_anterior = models.CharField(max_length=255)
    id_anterior = models.CharField(max_length=255)

    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_actualizado = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_cambio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Cambio de {self.producto} el {self.fecha_cambio}'