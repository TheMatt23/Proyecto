from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static  import	static
urlpatterns = [
    path('', views.pantalla_inicio, name='home'),  
    path('login/', views.login, name='login'),  
    path('sesion/', views.sesion, name='sesion'),
    path('add_usuario/', views.add_usuario, name='add_usuario'),
    path('loadministrador/', views.admin_home, name='admin_home'),  
    path('edit_item/<str:tipo>/<str:cedula>/', views.edit_item, name='edit_item'),
    path('delete_item/<str:tipo>/<str:cedula>/', views.delete_item, name='delete_item'),
]+static(settings.STATIC_URL,document_root=settings.STATICFILES_DIR)
