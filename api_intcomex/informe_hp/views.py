from django.shortcuts import render
import pandas as pd
from django.db import connection as conexion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
import numpy as np
import math
from datetime import datetime
import re
from io import BytesIO
# Create your views here.
@login_required
def importar(request): 
  try: 
    if request.method == "POST" and 'file1' in request.FILES:
     file = request.FILES["file1"]
     excel = pd.read_excel(file, sheet_name="Pedidos")
     excel1 = excel.replace(np.nan, "null")
     with conexion.cursor() as cursor:  
        consulta = "INSERT IGNORE INTO prueba(origen, numero_origen, cantidad, marca, sku_producto, nombre, apellidos, rut, direccion, ciudad, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        for index, row in excel1.iterrows():
          origen = row['Origen']
          numero_origen = row['Número de Origen']
          cantidad = row['Cantidad']
          marca = row['Marca']
          sku_producto= row['SKU producto']
          nombre = row['Nombre']
          apellidos = row['Apellidos']
          rut = row['RUT']
          direccion = row['Dirección línea 1']
          ciudad = row['Ciudad']
          region = row['Región / País']
          rows = [(origen, numero_origen, cantidad, marca, sku_producto, nombre, apellidos, rut, direccion, ciudad, region)]
          cursor.executemany(consulta, rows)
          #print(str(origen) + " " + str(numero_origen) + " " +str(cantidad) + " " + str(marca) + " " + str(sku_producto) + " " + str(nombre) + " " + str(apellidos) + " " + str(rut) + " " + str(direccion) + " " + str(ciudad) + " " + str(region))
    conexion.commit()
    messages.add_message(request, messages.SUCCESS, 'exito al cargar excel de centry')
  except ValueError:
    messages.add_message(request, messages.SUCCESS, 'formato del archivo incorrecto')
    conexion.close()
    
  return render(request, 'informe_hp/centry.html')

@login_required
def importarf(request): 
  try: 
    if request.method == "POST" and 'file2' in request.FILES:
      file_fac = request.FILES["file2"]
      excel_fac = pd.read_excel(file_fac, sheet_name="DETALLE")
      excel_fac1 = excel_fac.replace(np.nan,"null")
      with conexion.cursor() as cursor:  
        consulta = "INSERT IGNORE INTO prueba1(folio, fecha, rut, razon_social, direccion, numero) VALUES (%s, %s, %s, %s, %s, %s);"
        for index, row in excel_fac1.iterrows():
          folio = row['FOLIO']
          fecha_1 = row['FECHA']
          fecha = datetime.strptime(fecha_1, '%d-%m-%Y')
          rut = row['RUT']
          rut=re.sub('[.]','', rut)
          razon_social = row['RAZON SOCIAL']
          direccion= row['DIRECCIONCLIENTE']
          numero = row['AD 21']
          #print(str(folio) + " " + str(fecha) + " " + str(rut) + " " + str(razon_social) + " " + str(direccion) + " " + str(numero))    
          rows = [(folio, fecha, rut, razon_social, direccion, numero)]
          cursor.executemany(consulta, rows)
          #print(str(origen) + " " + str(numero_origen) + " " +str(cantidad) + " " + str(marca) + " " + str(sku_producto) + " " + str(nombre) + " " + str(apellidos) + " " + str(rut) + " " + str(direccion) + " " + str(ciudad) + " " + str(region))
      conexion.commit()
      messages.add_message(request, messages.SUCCESS, 'exito al cargar excel de facturacion')
  except ValueError:
      messages.add_message(request, messages.SUCCESS, 'formato del archivo incorrecto')
      conexion.close()
    
  return render(request, 'informe_hp/facturacion.html')  


def exportar(request):
    outfile = BytesIO()
    sql=('SELECT "AM60582" as "Reporter id", "Reparaciones BBCC Ltda." as "Reporter Company Name ", "10321657" as "Sell From Location ID (assigned by HP or Partner-assigned)", "Reparaciones BBCC Ltda." as "Sell from name","Paris 720" as "Sell From Address line 1", "Oficina 10" as "Sell From Address line 2","Santiago" as "Sell From City", "RM" as "Sell from State/Province Code", "8330138" as "Sell from postal code","CL" as "Sell from Country code",razon_social as "Ship To Customer Name", p.rut as "Ship To Company Tax ID",pr.direccion as "Ship To Address Line 1", "" as "Ship To Address Line 2", ciudad as "Ship To City", region as "Ship To State/Province Code", "8330138" as "Ship To Postal Code", p.rut as "Sold To Customer ID", cantidad as "Product Quantity Shipped/Sold",sku_producto as "Partner Reported Product ID", "" as "Product Description", "" as "Reseller’s Product Number", date_format(fecha, "%Y%m%d") AS "Channel Partner to Customer Transaction Date", folio as "Channel Partner to Customer Invoice ID", "Y" as "Drop Ship Flag", "" as "Sales Type", "Y" as Online, date_format(fecha, "%Y%m%d") as "Customer Online Order Date " FROM prueba1 as p join prueba as pr on p.rut=pr.rut where marca="hp";')
    df=pd.read_sql(sql, conexion)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    execl_name ='test'
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format(execl_name)
    df.to_excel(outfile, index=False)
    response.write(outfile.getvalue())
    
    return response  
