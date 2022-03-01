from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('importar/', views.importar, name="importar"),
    path('importarf/', views.importarf, name="importarf"),
    path('exportar/', views.exportar, name="exportar"),
]

