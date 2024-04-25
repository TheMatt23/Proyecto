from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from login.models import Terapia, Movimiento, TipoEjercicio
from .forms import TerapiaForm, MovimientoForm, TipoEjercicioForm

# Terapias
class TerapiaView(View):
    def get(self, request):
        # Mostrar todas las terapias
        terapias = Terapia.objects.all()
        tipo_ejercicios = TipoEjercicio.objects.all()

        terapia_form = TerapiaForm()  # Formulario para crear terapia
        tipo_ejercicio_form = TipoEjercicioForm()
    
        return render(request, 'terapia_view.html', {
            'terapias': terapias,
            'terapia_form': terapia_form,
            'tipo_ejercicios': tipo_ejercicios,
            'tipo_ejercicio_form': tipo_ejercicio_form,
        })


    def post(self, request):
        # Logica para determinar qué formulario se está enviando
        if 'add_terapia' in request.POST:
            terapia_form = TerapiaForm(request.POST)
            if terapia_form.is_valid():
                terapia_form.save()  # Guarda la nueva terapia

        elif 'add_tipo_ejercicio' in request.POST:
            tipo_ejercicio_form = TipoEjercicioForm(request.POST)
            if tipo_ejercicio_form.is_valid():
                tipo_ejercicio_form.save()  # Guarda el nuevo tipo de ejercicio
        
        # Redirigir a la misma vista después de procesar el formulario
        return redirect('terapia_view')  
    
class TerapiaDeleteView(View):
    def post(self, request, terapia_id):
        terapia = get_object_or_404(Terapia, pk=terapia_id)  
        terapia.delete()  # Eliminar la terapia
        return redirect('terapia_view')  
    
# Movimentos
class MovimientoAddView(View):
    def post(self, request, terapia_id):
        terapia = get_object_or_404(Terapia, pk=terapia_id)
        movimiento_form = MovimientoForm(request.POST)
        if movimiento_form.is_valid():
            # Asigna la terapia al movimiento antes de guardarlo
            movimiento = movimiento_form.save(commit=False)
            movimiento.terapiaID = terapia
            movimiento.save()  # Guarda el movimiento
        return redirect('terapia_view')  # Redirige a la misma página

# Vista para eliminar movimientos
class MovimientoDeleteView(View):
    def post(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
        movimiento.delete()  # Elimina el movimiento
        return redirect('terapia_view') 

class TipoEjercicioDeleteView(View):
    def post(self, request, tipo_ejercicio_id):
        tipo_ejercicio = get_object_or_404(TipoEjercicio, pk=tipo_ejercicio_id)
        tipo_ejercicio.delete()  # Elimina el tipo de ejercicio
        return redirect('terapia_view') 
