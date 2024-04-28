from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static  import	static
urlpatterns = [
    path('', views.login, name='login'),  # URL para la vista de inicio de sesión
    path('add_usuario/', views.add_usuario, name='add_usuario'),
    path('loadministrador/', views.admin_home, name='admin_home'),  # URL para la página de administrador
    path('edit_item/<str:tipo>/<str:cedula>/', views.edit_item, name='edit_item'),
    path('delete_item/<str:tipo>/<str:cedula>/', views.delete_item, name='delete_item'),
]+static(settings.STATIC_URL,document_root=settings.STATICFILES_DIR)
