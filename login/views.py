# Create your views here.
from django.shortcuts import render, redirect,  get_object_or_404
from django import forms
from .models import Admin
from .models import Fisioterapeuta, Paciente
from citaMedica.views import buscar_paciente as citaMedica 

from django.views.decorators.http import require_POST

@require_POST
def add_usuario(request):
    user_type = request.POST.get('user_type')
    cedula = request.POST.get('cedula')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    celular = request.POST.get('celular')
    direccion = request.POST.get('direccion')
    contrasena = request.POST.get('contrasena')

    if user_type == 'Fisioterapeuta':
        Fisioterapeuta.objects.create(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            direccion=direccion,
            contrasena=contrasena
        )
    elif user_type == 'Paciente':
        Paciente.objects.create(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            direccion=direccion,
            contrasena=contrasena
        )

    return redirect('admin_home') 
# Redirigir a la vista principal
def login(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        contrasena = request.POST.get('contrasena')
        
        try:
            admin = Admin.objects.get(cedula=cedula, contrasena=contrasena)
            return redirect('admin_home')  # Redirige a la página de administrador si las credenciales son correctas
        
        except Admin.DoesNotExist:
            try:
                fisioterapeuta = Fisioterapeuta.objects.get(cedula=cedula, contrasena=contrasena)
                request.session['fisioterapeuta_cedula'] = cedula  # Guarda la cédula del fisioterapeuta en la sesión
                return redirect('buscar_paciente', fisioterapeuta_cedula=cedula)  # Redirige a la página de búsqueda de paciente si las credenciales son correctas
            
            except Fisioterapeuta.DoesNotExist:
                # Aquí puedes agregar un mensaje de error si las credenciales no son correctas
                return render(request, 'sesion.html', {'error': 'Cédula o contraseña incorrecta'})

    return render(request, 'sesion.html')


            
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'celular', 'direccion']

class FisioterapeutaForm(forms.ModelForm):
    class Meta:
        model = Fisioterapeuta
        fields = ['nombre', 'apellido', 'celular', 'direccion']
        
def admin_home(request):
    filter_type = request.GET.get('filter', 'Fisioterapeutas')
    search_query = request.GET.get('search', '')

    if filter_type == 'Fisioterapeutas':
        items = Fisioterapeuta.objects.filter(cedula__icontains=search_query)
        tipo = 'Fisioterapeuta'
    else:
        items = Paciente.objects.filter(cedula__icontains=search_query)
        tipo = 'Paciente'

    context = {
        'items': items,
        'filter': filter_type,
        'tipo': tipo,
    }
    return render(request, 'administrador.html', context)



def edit_item(request, tipo, cedula):
    if tipo == 'Paciente':
        model_class = Paciente
        form_class = PacienteForm
    elif tipo == 'Fisioterapeuta':
        model_class = Fisioterapeuta
        form_class = FisioterapeutaForm
    else:
        return render(request, 'error.html', {'error': 'Tipo de usuario no válido'})

    item = get_object_or_404(model_class, cedula=cedula)
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('admin_home')  # Redirecciona a la vista principal
    else:
        form = form_class(instance=item)
    
    context = {
        'form': form,
        'tipo': tipo,
        'item': item,
    }
    return render(request, 'editarUser.html', context)

def delete_item(request, tipo, cedula):
    if tipo == 'Paciente':
        model_class = Paciente
    elif tipo == 'Fisioterapeuta':
        model_class = Fisioterapeuta
    else:
        # Manejo de error para tipo no válido
        return render(request, 'error.html', {'error': 'Tipo de usuario no válido'})

    # Obtener el objeto
    obj = get_object_or_404(model_class, cedula=cedula)

    # Eliminar el objeto
    obj.delete()

    return redirect('admin_home')  # Redirigir a la vista principal

def pantalla_inicio(request):
    return render(request, 'pantallaInicio.html')




def sesion(request):
    return render(request, 'sesion.html')
