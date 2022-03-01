from pyexpat import model
from django.db import models

# Create your models here.

class excel_centry(models.Model):
    origen = models.CharField(max_length=250)
    numero_origen = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    marca = models.CharField(max_length=250)
    sku_producto = models.CharField(max_length=250)
    nombre = models.CharField(max_length=250)
    apellidos = models.CharField(max_length=250)
    rut = models.CharField(max_length=250)
    direccion = models.CharField(max_length=250)
    ciudad = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    
    class Meta: #clase interna con representacion
        verbose_name = 'excel_centry'
        verbose_name_plural = 'excel_centrys'

    def __str__(self):
        return "{}".format(self.name)

class excel_factura(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField()
    rut  = models.CharField(max_length=250)
    razon_social = models.CharField(max_length=250)
    direccion = models.CharField(max_length=250)
    numero = models.CharField(max_length=250)    
    
    class Meta: #clase interna con representacion
        verbose_name = 'excel_factura'
        verbose_name_plural = 'excel_facturas'

    def __str__(self):
        return "{}".format(self.name)






























    






















 









