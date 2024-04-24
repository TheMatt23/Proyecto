from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # URL para la vista de inicio de sesión
    path('loadministrador/', views.admin_home, name='admin_home'),  # URL para la página de administrador
]
