from django.db import models

# Create your models here.
class producto(models.Model):
    sku = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=250)
    precio = models.IntegerField()
    marca = models.CharField(max_length=250)
    mpn = models.CharField(max_length=250)
    upc = models.CharField(max_length=250, null=True)
    peso = models.IntegerField()
    ancho = models.IntegerField()
    altura = models.IntegerField()
    largo = models.IntegerField()

    class Meta: #clase interna con representacion
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.sku
    
class imagenes(models.Model):
    descripcion = models.CharField(max_length=250)
    mpn = models.CharField(max_length=250)
    centralrencno = models.CharField(max_length=250)
    localSku = models.CharField(max_length=250, primary_key=True)
    descripcionfabrica = models.CharField(max_length=250)
    descripcionmarca = models.CharField(max_length=250)
    categoriacompleta = models.CharField(max_length=250)
    imagenes = models.CharField(max_length=250)
    longitud = models.CharField(max_length=250)
    altura = models.CharField(max_length=250)
    anchura = models.CharField(max_length=250)
    peso = models.CharField(max_length=250)
    profundidad = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'imagene'
        verbose_name_plural = 'imagenes'
          
class imagen_jumpseller(models.Model):
    id = models.IntegerField(primary_key=True)
    sku_imagen = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'imagen_jumpseller'
        verbose_name_plural = 'imagen_jumpsellers'
        
class imagen_mpn(models.Model):
    imagen = models.CharField(max_length=250)
    codigo = models.CharField(max_length=250, primary_key=True)
    cate = models.CharField(max_length=250)
    marcas = models.CharField(max_length=250)
    upc = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'imagen_mpn'
        verbose_name_plural = 'imagen_mpns'
        
class imagen_upc(models.Model):
    image = models.CharField(max_length=250)
    codigo = models.CharField(max_length=250, primary_key=True)
    cate = models.CharField(max_length=250)
    marcas = models.CharField(max_length=250)
    gti = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'imagen_upc'
        verbose_name_plural = 'imagen_upcs'