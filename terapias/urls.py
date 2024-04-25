from django.urls import path
from .views import TerapiaView, MovimientoAddView, MovimientoDeleteView, TerapiaDeleteView

urlpatterns = [
    path('', TerapiaView.as_view(), name='terapia_view'),
    path('deleteTerapia/<int:terapia_id>/', TerapiaDeleteView.as_view(), name='terapia_delete'),
    path('addMovimiento/<int:terapia_id>/', MovimientoAddView.as_view(), name='movimiento_add'),
    path('movimiento/delete/<int:movimiento_id>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
]
