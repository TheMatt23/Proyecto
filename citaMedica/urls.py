from django.urls import path, include
from . import views
from .views import TerapiaView, MovimientoAddView, MovimientoDeleteView, TerapiaDeleteView, TipoEjercicioDeleteView, AgregarEjercicioAMovimientoView, EliminarEjercicioView, ActualizarPorcentajeView

urlpatterns = [
    path('', views.buscar_paciente, name='generar_cita'),
    path('registro/', views.registrar_paciente, name='pacientes'),
    path('login/', include('login.urls')),
    path('<str:fisioterapeuta_cedula>/', views.buscar_paciente, name='buscar_paciente'), 
    path('terapias/ver-reporte/<int:terapia_id>/', views.ver_reporte, name='ver_reporte'),
    path('terapias/<str:cedula>/', TerapiaView.as_view(), name='terapia_view'),
    path('terapias/deleteTerapia/<int:terapia_id>/', TerapiaDeleteView.as_view(), name='terapia_delete'),
    path('terapia/<int:terapia_id>/movimiento/', views.ver_movimientos, name='ver_movimientos'),
    path('terapias/tipo-ejercicio/delete/<int:tipo_ejercicio_id>/', TipoEjercicioDeleteView.as_view(), name='tipo_ejercicio_delete'),
    path('movimiento/addMovimiento/<int:terapia_id>/', MovimientoAddView.as_view(), name='movimiento_add'),
    path('movimiento/delete/<int:movimiento_id>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
    path('movimiento/<int:movimiento_id>/agregar_ejercicio/', AgregarEjercicioAMovimientoView.as_view(), name='agregar_ejercicio_a_movimiento'),
    path('movimiento/ejercicio/delete/<int:ejercicio_id>/', EliminarEjercicioView.as_view(), name='eliminar_ejercicio'),
    path('movimiento/ejercicio/actualizar_porcentaje/', ActualizarPorcentajeView.as_view(), name='actualizar_porcentaje'),
    ]
