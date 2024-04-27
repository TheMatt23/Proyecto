from django.urls import path, include
from . import views
from .views import TerapiaView, MovimientoAddView, MovimientoDeleteView, TerapiaDeleteView, TipoEjercicioDeleteView, AgregarEjercicioAMovimientoView, EliminarEjercicioView

urlpatterns = [
    path('', views.buscar_paciente, name='generar_cita'),  # Ruta para generar citas
    path('login/', include('login.urls')),
    path('<str:fisioterapeuta_cedula>/', views.buscar_paciente, name='buscar_paciente'), # Ruta para la vista de citaMedica    
    path('terapias/', TerapiaView.as_view(), name='terapia_view'),
    path('terapias/deleteTerapia/<int:terapia_id>/', TerapiaDeleteView.as_view(), name='terapia_delete'),
    path('terapias/addMovimiento/<int:terapia_id>/', MovimientoAddView.as_view(), name='movimiento_add'),
    path('terapias/movimiento/delete/<int:movimiento_id>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
    path('terapias/tipo-ejercicio/delete/<int:tipo_ejercicio_id>/', TipoEjercicioDeleteView.as_view(), name='tipo_ejercicio_delete'),
    path('terapias/movimiento/<int:movimiento_id>/agregar-ejercicio/', AgregarEjercicioAMovimientoView.as_view(), name='agregar_ejercicio_a_movimiento'),
    path('terapias/ejercicio/eliminar/<int:ejercicio_id>/', EliminarEjercicioView.as_view(), name='eliminar_ejercicio'),  # Ruta para eliminar ejercicio
]
