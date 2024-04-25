from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from login.models import Terapia, Movimiento
from .forms import TerapiaForm, MovimientoForm

# Terapias
class TerapiaView(View):
    def get(self, request):
        # Mostrar todas las terapias
        terapias = Terapia.objects.all()
        terapia_form = TerapiaForm()  # Formulario para crear terapia
        return render(request, 'terapia_view.html', {'terapias': terapias, 'terapia_form': terapia_form})

    def post(self, request):
        # Crear nueva terapia
        terapia_form = TerapiaForm(request.POST)
        if terapia_form.is_valid():
            terapia_form.save()  # Guarda la nueva terapia
        return redirect('terapia_view')  # Redirige a la misma página
    
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