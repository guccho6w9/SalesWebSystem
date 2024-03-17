from django.db import models
from django.utils import timezone

# Create your models here.

class Producto(models.Model):
    id_pd = models.AutoField(primary_key=True)
    cod = models.CharField(max_length=20)
    des = models.CharField(max_length=75, blank=False)
    stock = models.IntegerField(default=0)
    pre = models.FloatField(blank=False)
    aju = models.CharField(max_length=4, blank=False)
    ofe = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return f"{self.cod} {self.des} {self.pre} {self.aju} {self.ofe} {self.stock}"
    

    
from django.core.serializers.json import DjangoJSONEncoder

class ProductoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Producto):
            # Convert the Producto object to a dictionary
            return {
                'id_pd': obj.id_pd,
                'cod': obj.cod,
                'des': obj.des,
                'pre': obj.pre,
                'stock': obj.stock,

                
                # Add other fields as needed
            }
        return super().default(obj)


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
    

class FacturaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.des} - ${self.producto.pre} c/u"

    def subtotal(self):
        return self.cantidad * self.producto.pre
    


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    condicion_venta = models.CharField(max_length=100)
    condicion_fiscal = models.CharField(max_length=100)
    cuit_dni = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    

class HistorialFactura(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()
    nombre_cliente = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    condicion_venta = models.CharField(max_length=100, default="efectivo")
    condicion_fiscal = models.CharField(max_length=100, default="Arg.Consumidor Final")  # Nuevo campo
    cuit_dni = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.producto} - {self.cantidad} - {self.fecha}"