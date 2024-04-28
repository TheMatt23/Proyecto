from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', include('login.urls')),
    path('<str:paciente_cedula>/', views.paciente_detalle, name='paciente_detalle'),
    path('grafico/ver-reporte/<int:terapia_id>/', views.ver_reporte, name='ver_reporte'),
    path('grafico/reporte-general/<str:cedula_paciente>/', views.reporte_general, name='reporte_general'),  # Correcto
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]
