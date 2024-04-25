from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', include('login.urls')),
    path('<str:fisioterapeuta_cedula>/', views.buscar_paciente, name='buscar_paciente'), # Ruta para la vista de citaMedica
    path('', views.buscar_paciente, name='generar_cita'),  # Ruta para generar citas
]
