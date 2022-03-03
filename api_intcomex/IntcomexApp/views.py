from email import message
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection as conexion
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from api_intcomex.settings import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from IntcomexApp.models import producto
from IntcomexApp.forms import ProductoForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
import hashlib
from datetime import datetime
import requests
import json
import numpy as np
import math
import re
from io import BytesIO
import pandas as pd



apikey = "c4fb951e-620c-4359-a3a9-f1e79e1d7392"
hora_actual = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
firma = apikey+",0d1a7366-a9db-444e-84f0-41539993b16e,"+hora_actual
h = hashlib.sha256(firma.encode('utf-8'))
apikey2 = "a014de3f594f4f78b44088137cdef12fb1539577"
forma = "json"

response= requests.get("https://intcomex-prod.apigee.net/v1/getcatalog?", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()})
dataJson=response.json
#print(response.content)
jsonToPython = json.loads(response.content)

response2= requests.get("http://api.cmfchile.cl/api-sbifv3/recursos_api/dolar?", params = {"apikey":apikey2,"formato":forma})
dataJson2=response2.json
#print(response.content)
jsonToPython2 = json.loads(response2.content)
try:
    valor_dolar=jsonToPython2['Dolares'][0]['Valor'].replace(",",".")
except KeyError:
    valor_dolar="900.00"

response3= requests.get("https://intcomex-prod.apigee.net/v1/downloadextendedcatalog?", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()})
dataJson3=response3.json
#print(response.content)
jsonToPython3 = json.loads(response3.content)

#login = "5d03f313380c95128175b708390e7b92"
#authtoken = "02bd20a4903bc44efc4298e2d84659ff"
login = "04490abd35c41fcab3af6c7e5bd2f63f"
authtoken = "f34b373f8974c16b5b945fc9a6c0f952"
response4 = requests.get("https://api.jumpseller.com/v1/products/category/1138476.json?", params = {"login":login,"authtoken":authtoken}, headers= {"Content-Type":"application/json"})
# Definimos la cabecera y el diccionario con los datos
dataJson4=response4.json
#print(response.content)
jsonToPython4 = json.loads(response4.content)
    

# Create your views here
@login_required
def intcomex(request):
    return render(request, "IntcomexApp/crud_intcomex.html")

def insert_dash(string, index):
    return string[:index] + '.' + string[index:]
    
@login_required
def agregar(request):
    request.method=="POST"
     
    with conexion.cursor() as cursor:
        
        consulta = "INSERT IGNORE INTO intcomexapp_producto(sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        for x in range(0,len(jsonToPython)):
            sku=jsonToPython[x]['Sku']
            mpn=jsonToPython[x]['Mpn']
            descripcion=jsonToPython[x]['Description']
            cantidad=jsonToPython[x]['InStock']
            categoria=jsonToPython[x]['Category']['Description']
            antigua=round(((jsonToPython[x]['Price']['UnitPrice']*float(valor_dolar))*1.19)*1.10)
            otra=str(antigua)
            nueva=insert_dash(otra, -3)
            nueva1=nueva[:-3]
            precios =nueva1.replace(".", "990")
            try:
                precio = int(precios)
            except ValueError:
                print("")
            marca=jsonToPython[x]['Manufacturer']['Description']
            upc=jsonToPython[x]['Upc']
            
            try:
                peso=round(jsonToPython[x]['Freight']['Package']['Weight']*0.453592)
            except TypeError:
                peso=0
            try:
                ancho=round(jsonToPython[x]['Freight']['Package']['Width']*2.54)
            except TypeError:
                ancho=0
            try:
                altura=round(jsonToPython[x]['Freight']['Package']['Height']*2.54)
            except TypeError:
                altura=0
            try:
                largo=round(jsonToPython[x]['Freight']['Package']['Length']*2.54)
            except TypeError:
                largo=0
            rows = [(sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo)]
            if cantidad > 5 and precio > 1:
                cursor.executemany(consulta, rows) 
            else:
                print("No hay lo suficiente") 
                print(rows)
        conexion.commit()
    
        conexion.close()
        
    return render(request, "IntcomexApp/crud_intcomex.html")
    
@login_required
def actualizar(request):  
    try:
        with conexion.cursor() as cursor:
             consulta = "UPDATE intcomexapp_producto SET CANTIDAD = %s, PRECIO = %s WHERE sku = %s;"
             for x in range(0,len(jsonToPython)):
                cantidad=jsonToPython[x]['InStock']
                antigua=round(((jsonToPython[x]['Price']['UnitPrice']*float(valor_dolar))*1.19)*1.10)
                otra=str(antigua)
                nueva=insert_dash(otra, -3)
                nueva1=nueva[:-3]
                precios =nueva1.replace(".", "990")
                try:
                    precio = int(precios)
                except ValueError:
                    print("")
                sku=jsonToPython[x]['Sku']
                cursor.execute(consulta, (cantidad, precio, sku))
             conexion.commit()  
    finally:
             conexion.close()
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def agregar_imagen(request):
    request.method=="POST"
    
    response3= requests.get("https://intcomex-prod.apigee.net/v1/downloadextendedcatalog?", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()})
    dataJson3=response3.json
    #print(response.content)
    jsonToPython3 = json.loads(response3.content)
    
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT IGNORE INTO intcomexapp_imagenes(descripcion, mpn, centralrencno, localSku, descripcionfabrica, descripcionmarca, categoriacompleta, imagenes, longitud, altura, anchura, peso, profundidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            for x in range(0,len(jsonToPython3)):
                descripcion=jsonToPython3[x]['Descripcion']
                mpn=jsonToPython3[x]['mpn']
                centralrencno=jsonToPython3[x]['centralRecno']
                localSku=jsonToPython3[x]['localSku']
                descripcionfabrica=jsonToPython3[x]['DescripcionFabrica']
                descripcionmarca=jsonToPython3[x]['DescripcionMarca']
                categoriacompleta=jsonToPython3[x]['CategoriaCompleta']
                try:
                    imagenes=jsonToPython3[x]['Imagenes'][0]['url']
                    imagenes=jsonToPython3[x]['Imagenes'][1]['url']
                except IndexError:
                    imagenes=None
                try:
                    longitud=jsonToPython3[x]['Dimensiones y peso / Longitud'] 
                    longitud = str(longitud)
                except KeyError:
                    longitud=None
                try:
                    altura=jsonToPython3[x]['Dimensiones y peso / Altura']
                    altura = str(altura)
                except KeyError:
                    altura=None
                try:
                    anchura=jsonToPython3[x]['Dimensiones y peso / Anchura']
                    anchura = str(anchura)
                except KeyError:
                    anchura=None
                try:
                    peso=jsonToPython3[x]['Dimensiones y peso / Peso']
                    peso = str(peso)
                except KeyError:
                    peso=None
                try:
                    profundidad=jsonToPython3[x]['Dimensiones y peso / Profundidad']
                    profundidad = str(profundidad)
                except KeyError:
                    profundidad=None
                rows = [(descripcion, mpn, centralrencno, localSku, descripcionfabrica, descripcionmarca, categoriacompleta, imagenes, longitud, altura, anchura, peso, profundidad)]
                print(rows)
                cursor.executemany(consulta, rows) 
        conexion.commit()
    finally:
        conexion.close()
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def imagen_mpn(request):
    try:  
        cursor_mpn = conexion.cursor()
        query=("SELECT marca, mpn, categoria FROM  intcomexapp_producto")
        cursor_mpn.execute(query)
        for marca, mpn, categoria in cursor_mpn.fetchall():
            UserName="openIcecat-live"
            Language="en"
            response_mpn= requests.get("https://live.icecat.biz/api/?", params = {"UserName":UserName,"Language":Language,"Brand":marca,"ProductCode":mpn})
            dataJson_mpn=response_mpn.json
            #print(response.content)
            jsonToPython_mpn = json.loads(response_mpn.content)
            cursor_mpn1= conexion.cursor() 
            consulta = "INSERT IGNORE INTO intcomexapp_imagen_mpn(imagen, codigo, cate, marcas, upc) VALUES (%s, %s, %s, %s, %s);"
            try:
                imagen=jsonToPython_mpn['data']['Image']['HighPic']
                codigo=mpn
                cate=categoria
                marcas=marca
                try:
                    upc=jsonToPython_mpn['data']['GeneralInfo']['GTIN'][0]
                except IndexError:
                    upc="null"
            except KeyError:
                imagen="null"
                codigo=mpn
                cate=categoria
                marcas=marca
                upc="null"
            rows = [(imagen, codigo, cate, marcas, upc)]
            print(rows)
            cursor_mpn1.executemany(consulta, rows) 
        conexion.commit()
    finally:
        conexion.close()
            
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def imagen_ucp(request): 
    try: 
        cursor_upc = conexion.cursor()
        query=("SELECT marca, mpn, categoria, upc FROM  intcomexapp_producto")
        cursor_upc.execute(query)
        for marca, mpn, categoria, upc in cursor_upc.fetchall():
            UserName="openIcecat-live"
            Language="en"
            response_upc= requests.get("https://live.icecat.biz/api/?", params = {"UserName":UserName,"Language":Language,"GTIN":upc})
            dataJson_upc=response_upc.json
            #print(response.content)
            jsonToPython_upc = json.loads(response_upc.content)
            cursor_upc1= conexion.cursor() 
            consulta = "INSERT IGNORE INTO intcomexapp_imagen_upc(image, codigo, cate, marcas, gti) VALUES (%s, %s, %s, %s, %s);"
            try:
                image=jsonToPython_upc['data']['Image']['HighPic']
                codigo=mpn
                cate=categoria
                marcas=marca
                try:
                    gti=jsonToPython_upc['data']['GeneralInfo']['GTIN'][0]
                except IndexError:
                    gti="null"
            except KeyError:
                image="null"
                codigo=mpn
                cate=categoria
                marcas=marca
                gti="null"
            rows = [(image, codigo, cate, marcas, gti)]
            print(rows)
            cursor_upc1.executemany(consulta, rows) 
        conexion.commit()
    finally:
        conexion.close()
            
    return render(request, "IntcomexApp/crud_intcomex.html")
    
@login_required            
def actualizar_imagen_mpn(request):
    cursor_act_mpn = conexion.cursor()
    try:
        query=("SELECT codigo, image, gti FROM  intcomexapp_imagen_upc")
        cursor_act_mpn.execute(query)
        for codigo, image ,gti in cursor_act_mpn.fetchall():
            conexion
            consulta = "UPDATE intcomexapp_imagen_mpn SET imagen = %s WHERE codigo = %s and imagen='null';"
            cursor_act_mpn1= conexion.cursor()
            cursor_act_mpn1.execute(consulta, (image, codigo))
        conexion.commit()
        print("exito")
    finally:
        conexion.close()
    
    return render(request, "IntcomexApp/crud_intcomex.html")
 
@login_required        
def actualizar_upc(request):
    cursor_act_upc = conexion.cursor()
    try:
        query=("SELECT codigo, upc FROM intcomexapp_imagen_mpn WHERE upc<>'null';")
        cursor_act_upc.execute(query)
        for codigo, upc in cursor_act_upc.fetchall():
            conexion
            consulta = "UPDATE intcomexapp_producto SET upc = %s WHERE mpn = %s and upc='';"
            cursor_act_upc1= conexion.cursor()
            cursor_act_upc1.execute(consulta, (upc, codigo))
        conexion.commit()
        print("exito")
    finally:
        conexion.close()
        
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def actualizar_imagen(request):
    cursor_imagen = conexion.cursor()
    try:
        query=("SELECT codigo, imagen FROM  intcomexapp_imagen_mpn where imagen<>'null'")
        cursor_imagen.execute(query)
        for codigo, imagen in cursor_imagen.fetchall():
            conexion
            consulta = "UPDATE intcomexapp_imagenes SET imagenes = %s WHERE mpn = %s and imagenes='';"
            cursor_imagen1= conexion.cursor()
            cursor_imagen1.execute(consulta, (imagen, codigo))
        conexion.commit()
        print("exito")
    finally:
        conexion.close()
        
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def sin_imagen(request):
    cursor = conexion.cursor()
    try:
        query=("UPDATE intcomexapp_imagenes SET imagenes = %s WHERE imagenes='a';")
        imagen = " "
        cursor.execute(query, (imagen))
        conexion.commit()  
    finally:
        conexion.close()
    
    return render(request, "IntcomexApp/crud_intcomex.html")
    
    
@login_required
def agregar_j(request):
    try:
        cur = conexion.cursor()
        cur.execute( "SELECT sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo FROM intcomexapp_producto as p WHERE NOT EXISTS (SELECT NULL FROM intcomexapp_imagen_jumpseller as i WHERE p.sku= i.sku_imagen)" )
        for sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo in cur.fetchall():
            data = {"product": {
            "name": descripcion,
            "description": descripcion + " - " + sku + " #No Sanday",
            "page_title": descripcion,
            "meta_description": "Productos",
            "price": precio,
            "weight": peso,
            "stock": cantidad,
            "stock_unlimited": False,
            "sku": mpn,
            "barcode": upc,
            "google_product_category": "",
            "brand": marca,
            "featured": False,
            "shipping_required": True,
            "status": "available",
            "package_format": "box",
            "length": largo,
            "width": ancho,
            "height": altura,
            "diameter": 0,
            "permalink": mpn,
            "categories": [
            {
            "id": 2,
            "name": categoria,
            "parent_id": 0,
            "permalink": categoria
            }
            ]
            }
            }
            #login = "5d03f313380c95128175b708390e7b92"
            #authtoken = "02bd20a4903bc44efc4298e2d84659ff"
            login = "04490abd35c41fcab3af6c7e5bd2f63f"
            authtoken = "f34b373f8974c16b5b945fc9a6c0f952"
            response1 = requests.post("https://api.jumpseller.com/v1/products.json?", params = {"login":login,"authtoken":authtoken}, headers= {"Content-Type":"application/json"}, data = json.dumps(data))
            # Definimos la cabecera y el diccionario con los datos
            dataJson1=response1.json
            #print(response.content)
            jsonToPython1 = json.loads(response1.content)
            #if response1.status_code == 200:
            # print (response1.text)
            #print (sku, descripcion, cantidad, categoria, precio)
    finally:
         conexion.close()
        
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def agregar_id(request):
    
    login = "04490abd35c41fcab3af6c7e5bd2f63f"
    authtoken = "f34b373f8974c16b5b945fc9a6c0f952"
    response7 = requests.get("https://api.jumpseller.com/v1/products/count.json?", params = {"login":login,"authtoken":authtoken}, headers= {"Content-Type":"application/json"})
    dataJson7=response7.json
    jsonToPython7 = json.loads(response7.content)
    contar=jsonToPython7['count']
    total=math.ceil(contar/100)
    limit = 200
    for page in range(total):
        response4 = requests.get("https://api.jumpseller.com/v1/products.json?", params = {"login":login,"authtoken":authtoken, "limit":limit, "page":page}, headers= {"Content-Type":"application/json"})
        # Definimos la cabecera y el diccionario con los datos
        dataJson4=response4.json
        #print(response.content)
        jsonToPython4 = json.loads(response4.content)
        try:
            with conexion.cursor() as cursor:
                consulta = "INSERT IGNORE INTO intcomexapp_imagen_jumpseller(id, sku_imagen) VALUES (%s, %s);"
                for x in range(0,len(jsonToPython4)):
                    id=jsonToPython4[x]['product']['id']
                    sku_imagen=jsonToPython4[x]['product']['sku']
                    rows = [(id, sku_imagen)]
                    cursor.executemany(consulta, rows) 
            conexion.commit()
        finally:
            conexion.close()

    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def enviar_imagen(request):
    cur = conexion.cursor()
    try:
        cur.execute("SELECT id, sku_imagen, imagenes FROM intcomexapp_imagen_jumpseller join intcomexapp_imagenes on intcomexapp_imagenes.mpn = intcomexapp_imagen_jumpseller.sku_imagen")
        for id, sku_imagen, imagenes in cur.fetchall():
            data = {
            "image": {
            "url": imagenes
            }
            }
            #login = "5d03f313380c95128175b708390e7b92"
            #authtoken = "02bd20a4903bc44efc4298e2d84659ff"
            login = "04490abd35c41fcab3af6c7e5bd2f63f"
            authtoken = "f34b373f8974c16b5b945fc9a6c0f952"
            response = requests.post("https://api.jumpseller.com/v1/products/"+str(id)+"/images.json?", params = {"login":login,"authtoken":authtoken}, headers= {"Content-Type":"application/json"}, data = json.dumps(data))
            dataJson=response.json
            jsonToPython = json.loads(response.content)
            print(jsonToPython)
    finally:      
        conexion.close()

    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def actualiza_jumpseller(request):
    try:
        cur = conexion.cursor()
        cur.execute("SELECT sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo, id  FROM intcomexapp_producto join intcomexapp_imagen_jumpseller on intcomexapp_producto.mpn = intcomexapp_imagen_jumpseller.sku_imagen")
        for sku, descripcion, cantidad, categoria, precio, marca, mpn, upc, peso, ancho, altura, largo, id in cur.fetchall():
            data ={
            "product": {
            "name": descripcion,
            "description": descripcion + " - " + sku + " #No Sanday",
            "page_title": descripcion,
            "meta_description": "Productos",
            "price": precio,
            "weight": peso,
            "stock": cantidad,
            "stock_unlimited": False,
            "sku": mpn,
            "barcode": upc,
            "google_product_category": "",
            "brand": marca,
            "featured": False,
            "shipping_required": True,
            "status": "available",
            "package_format": "box",
            "length": largo,
            "width": ancho,
            "height": altura,
            "diameter": 0,
            "permalink": mpn,
            "categories": [
            {
            "id": 2,
            "name": categoria,
            "parent_id": 0,
            "permalink": categoria
            }
            ]
            }
            }
            #login = "5d03f313380c95128175b708390e7b92"
            #authtoken = "02bd20a4903bc44efc4298e2d84659ff"
            login = "04490abd35c41fcab3af6c7e5bd2f63f"
            authtoken = "f34b373f8974c16b5b945fc9a6c0f952"
            response = requests.put("https://api.jumpseller.com/v1/products/"+str(id)+".json?", params = {"login":login,"authtoken":authtoken}, headers= {"Content-Type":"application/json"}, data = json.dumps(data))
            dataJson=response.json
            jsonToPython = json.loads(response.content)
            print(jsonToPython)
    finally:
        conexion.close()

    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def enviar_ordenes(request):
    orden = 'orden' in request.POST
    """
    #select * from ordenes as o where exists (select * from intcomexapp_producto as i where o.sku = i.sku );
    cur = conexion.cursor()
    query=("SELECT id, fecha, sku, unidad FROM ordenes where id=(%s)")
    cur.execute(query, orden)
    for id, fecha, sku, unidad in cur.fetchall():
        if sku[-3:]=="RUS":
            sku=sku[:-3]"""
    data = {
    "CustomerOrderNumber": orden,
    "Tag": "VipOrder",
    "Items": [
    {
    "Sku": "ID010MSR51",
    "Quantity": 1
    }
    ]
    }
    apikey = "b315098a-260f-4785-b612-a7a504e428d8"
    hora_actual = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    firma = apikey+",9bbd0af7-fb5d-48b7-9afd-b5f2908ce93a,"+hora_actual
    h = hashlib.sha256(firma.encode('utf-8'))

    response= requests.post("https://intcomex-test.apigee.net/v1/placeorder", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()}, headers= {"Content-Type":"application/json"}, data = json.dumps(data))
    dataJson=response.json
    #print(response.content)
    jsonToPython = json.loads(response.content)
    print(jsonToPython)
    messages.add_message(request, messages.SUCCESS, 'enviado')
    #conexion.close()
      
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def recuperar_orden(request):
    orden = 'orden' in request.POST
    apikey = "b315098a-260f-4785-b612-a7a504e428d8"
    hora_actual = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    firma = apikey+",9bbd0af7-fb5d-48b7-9afd-b5f2908ce93a,"+hora_actual
    h = hashlib.sha256(firma.encode('utf-8'))

    response= requests.get("https://intcomex-test.apigee.net/v1/getorder", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest(), "OrderNumber":orden}, headers= {"Content-Type":"application/json"})
    dataJson=response.json
    #print(response.content)
    jsonToPython = json.loads(response.content)

    norden=jsonToPython['OrderNumber']
    fecha_orden=jsonToPython['OrderDate']
    print(norden + " " + str(fecha_orden))
    
    return render(request, "IntcomexApp/crud_intcomex.html")

@login_required
def exportar_errores(request):
    outfile = BytesIO()
    sql=('SELECT i.sku, i.upc, i.descripcion, i.cantidad, i.marca, i.peso, i.ancho, i.altura, i.largo, i.mpn, i.categoria, p.imagenes FROM intcomexapp_producto as i LEFT join prueba_imagenes as p on i.sku=p.localSku;')
    df=pd.read_sql(sql, conexion)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    execl_name ='vacios'
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format(execl_name)
    df.to_excel(outfile, index=False)
    response.write(outfile.getvalue())
    
    return response  

@login_required
def listar_producto(request):
    productos= producto.objects.all()
    page = request.GET.get('page', 1)
    try: 
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404
    
    
    data = {
        'entity': productos,
        'paginator': paginator
    }
    
    return render(request, "IntcomexApp/listar.html", data)

@login_required
def modificar_producto(request, sku):
    
    Producto = get_object_or_404(producto, sku=sku)
    
    data = {
        'form': ProductoForm(instance=Producto)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=Producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="listar_producto")
        data["form"] = formulario
    
    return render(request, "IntcomexApp/modificar.html", data)