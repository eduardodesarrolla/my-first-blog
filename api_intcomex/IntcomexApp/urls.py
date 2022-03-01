from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('intcomex/', views.intcomex, name="intcomex"),
    path('agregar/', views.agregar, name="agregar"),
    path('actualizar/', views.actualizar, name="actualizar"),
    path('agregar_j/', views.agregar_j, name="agregar_j"),
    path('agregar_imagen/', views.agregar_imagen, name="agregar_imagen"),
    path('enviar_imagen/', views.enviar_imagen, name="enviar_imagen"),
    path('agregar_id/', views.agregar_id, name="agregar_id"),
    path('actualiza_jumpseller/', views.actualiza_jumpseller, name="actualiza_jumpseller"),
    path('enviar_ordenes/', views.enviar_ordenes, name="enviar_ordenes"),
    path('recuperar_orden/', views.recuperar_orden, name="recuperar_orden"),
    path('imagen_mpn/', views.imagen_mpn, name="imagen_mpn"),
    path('imagen_ucp/', views.imagen_ucp, name="imagen_upc"),
    path('actualizar_imagen_mpn/', views.actualizar_imagen_mpn, name="actualizar_imagen_mpn"),
    path('actualizar_upc/', views.actualizar_upc, name="actualizar_upc"),
    path('actualizar_imagen/', views.actualizar_imagen, name="actualizar_imagen"),
    path('exportar_errores/', views.exportar_errores, name="exportar_errores"),
   
]
