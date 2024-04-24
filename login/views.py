from django.shortcuts import render, redirect
from .models import Admin
from .models import Fisioterapeuta, Paciente

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
    filter_type = request.GET.get('filter', 'Fisioterapeutas')
    search_query = request.GET.get('search', '')

    if filter_type == 'Fisioterapeutas':
        items = Fisioterapeuta.objects.filter(cedula__icontains=search_query)
    else:
        items = Paciente.objects.filter(cedula__icontains=search_query)

    context = {
        'items': items,
        'filter': filter_type,
    }
    return render(request, 'administrador.html', context)

def edit_item(request, cedula):
    try:
        fisioterapeuta = Fisioterapeuta.objects.get(cedula=cedula)
        # Aquí puedes agregar la lógica para editar el fisioterapeuta
        return render(request, 'editar_fisioterapeuta.html', {'fisioterapeuta': fisioterapeuta})
    except Fisioterapeuta.DoesNotExist:
        try:
            paciente = Paciente.objects.get(cedula=cedula)
            # Aquí puedes agregar la lógica para editar el paciente
            return render(request, 'editar_paciente.html', {'paciente': paciente})
        except Paciente.DoesNotExist:
            return render(request, 'error.html', {'error': 'El usuario no existe'})


def delete_item(request, cedula):
    try:
        fisioterapeuta = Fisioterapeuta.objects.get(cedula=cedula)
        fisioterapeuta.delete()
        return redirect('admin_home')
    except Fisioterapeuta.DoesNotExist:
        try:
            paciente = Paciente.objects.get(cedula=cedula)
            paciente.delete()
            return redirect('admin_home')
        except Paciente.DoesNotExist:
            return render(request, 'error.html', {'error': 'El usuario no existe'})

