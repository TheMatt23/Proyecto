from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_paciente, name='generar_cita'),  # Ruta para generar citas
    path('terapias/<int:cita_id>/', views.terapias, name='terapias'),  # Ruta para vista 'terapias' con cita_id
]