from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # URL para la vista de inicio de sesión
    path('loadministrador/', views.admin_home, name='admin_home'),  # URL para la página de administrador
    path('edit/<str:cedula>/', views.edit_item, name='edit_item'),  # URL para editar
    path('delete/<str:cedula>/', views.delete_item, name='delete_item'),  # URL para eliminar
]
