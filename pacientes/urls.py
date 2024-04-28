from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas URL aquí...
    path('paciente-detalle/', views.paciente_detalle, name='paciente_detalle'),
     path('ver-reporte/<int:terapia_id>/', views.ver_reporte, name='ver_reporte'),
path('reporte-general/', views.reporte_general, name='reporte_general'),
    # Otras rutas URL aquí...
]
