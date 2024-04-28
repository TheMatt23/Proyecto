from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas URL aquí...
    path('paciente-detalle/', views.paciente_detalle, name='paciente_detalle'),
    # Otras rutas URL aquí...
]
