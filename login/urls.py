from django.urls import path
from . import views

urlpatterns = [
    path('', views.pantalla_inicio, name='home'),  
    path('login/', views.login, name='login'),  
    path('sesion/', views.sesion, name='sesion'),  # Define la ruta para la página de inicio de sesión
    path('add_usuario/', views.add_usuario, name='add_usuario'),
    path('loadministrador/', views.admin_home, name='admin_home'),  
    path('edit_item/<str:tipo>/<str:cedula>/', views.edit_item, name='edit_item'),
    path('delete_item/<str:tipo>/<str:cedula>/', views.delete_item, name='delete_item'),
]
