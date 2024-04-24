from django.shortcuts import render, redirect
from .models import Admin

def login(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        contrasena = request.POST.get('contrasena')
        
        try:
            admin = Admin.objects.get(cedula=cedula, contrasena=contrasena)
            return redirect('admin_home')  # Redirige a la página de administrador si las credenciales son correctas
        except Admin.DoesNotExist:
            # Aquí puedes agregar un mensaje de error si las credenciales no son correctas
            return render(request, 'sesion.html', {'error': 'Cédula o contraseña incorrecta'})

    return render(request, 'sesion.html')

def admin_home(request):
    return render(request, 'administrador.html')
