from django.urls import path
from .views import TerapiaView, MovimientoAddView, MovimientoDeleteView, TerapiaDeleteView, TipoEjercicioDeleteView, AgregarEjercicioAMovimientoView, EliminarEjercicioView

urlpatterns = [
    path('', TerapiaView.as_view(), name='terapia_view'),
    path('deleteTerapia/<int:terapia_id>/', TerapiaDeleteView.as_view(), name='terapia_delete'),
    path('addMovimiento/<int:terapia_id>/', MovimientoAddView.as_view(), name='movimiento_add'),
    path('movimiento/delete/<int:movimiento_id>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
    path('tipo-ejercicio/delete/<int:tipo_ejercicio_id>/', TipoEjercicioDeleteView.as_view(), name='tipo_ejercicio_delete'),
    path('movimiento/<int:movimiento_id>/agregar-ejercicio/', AgregarEjercicioAMovimientoView.as_view(), name='agregar_ejercicio_a_movimiento'),
    path('ejercicio/eliminar/<int:ejercicio_id>/', EliminarEjercicioView.as_view(), name='eliminar_ejercicio'),  # Ruta para eliminar ejercicio

]