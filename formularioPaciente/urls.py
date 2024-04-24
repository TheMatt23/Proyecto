from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_paciente),
    path('menu/', views.menu, name='menu'),  # Nueva URL para redirigir después de guardar
]