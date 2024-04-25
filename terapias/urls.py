from django.urls import path
from .views import TerapiaView, MovimientoAddView, MovimientoDeleteView, TerapiaDeleteView, TipoEjercicioView, TipoEjercicioAddView, TipoEjercicioDeleteView
urlpatterns = [
    path('', TerapiaView.as_view(), name='terapia_view'),
    path('deleteTerapia/<int:terapia_id>/', TerapiaDeleteView.as_view(), name='terapia_delete'),
    path('addMovimiento/<int:terapia_id>/', MovimientoAddView.as_view(), name='movimiento_add'),
    path('movimiento/delete/<int:movimiento_id>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
    path('tipo-ejercicio/', TipoEjercicioView.as_view(), name='tipo_ejercicio_view'),  # Vista para mostrar el modal
    path('tipo-ejercicio/add/', TipoEjercicioAddView.as_view(), name='tipo_ejercicio_add'),  # Ruta para agregar tipos de ejercicio
    path('tipo-ejercicio/delete/<int:tipo_ejercicio_id>/', TipoEjercicioDeleteView.as_view(), name='tipo_ejercicio_delete')
]
