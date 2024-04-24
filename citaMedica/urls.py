from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_paciente, name='generar_cita'),  # Ruta para generar citas
    #path('exito/', views.exito, name='exito'),  # Ruta para la página de éxito después de guardar
]
