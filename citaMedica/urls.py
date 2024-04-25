from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_paciente, name='generar_cita'),  # Ruta para generar citas
]
