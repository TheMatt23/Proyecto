from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from login.models import Paciente, Fisioterapeuta, CitaMedica, Terapia, TipoEjercicio, Movimiento, Ejercicios
from .forms import BuscarPacienteForm, CitaMedicaForm, AgregarTerapiaForm, EliminarCitaForm, TerapiaForm, TerapiaForm, MovimientoForm, TipoEjercicioForm, EjercicioComboForm
import datetime

def buscar_paciente(request, fisioterapeuta_cedula=None):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    cita_form = CitaMedicaForm(request.POST or None)
    eliminar_cita_form = EliminarCitaForm(request.POST or None)
    agregar_terapia_form = AgregarTerapiaForm(request.POST or None)

    if fisioterapeuta_cedula:
        try:
            # Obtener el fisioterapeuta conectado
            fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula=fisioterapeuta_cedula)

            if request.method == 'POST':
                if 'crear_cita' in request.POST and search_form.is_valid():
                    cedula = search_form.cleaned_data['cedula']
                    try:
                        paciente = Paciente.objects.get(cedula=cedula)
                        context['paciente'] = paciente

                        nueva_cita = CitaMedica(
                            cedulaPaciente=paciente,
                            cedulaFisioterapeuta=fisioterapeuta_conectado,
                            fecha=datetime.date.today()  # Fecha actual
                        )
                        nueva_cita.save()

                    except Paciente.DoesNotExist:
                        context['error_message'] = "Paciente no encontrado."

                if 'eliminar_cita' in request.POST and eliminar_cita_form.is_valid():
                    cita_id = eliminar_cita_form.cleaned_data['cita_id']
                    CitaMedica.objects.filter(pk=cita_id).delete()

                if 'agregar_terapia' in request.POST and agregar_terapia_form.is_valid():
                    return JsonResponse({'message': 'Terapia agregada exitosamente.'})  # Respuesta para AJAX

            if search_form.is_valid():
                cedula = search_form.cleaned_data['cedula']
                try:
                    paciente = Paciente.objects.get(cedula=cedula)
                    context['paciente'] = paciente

                    citas_medicas = CitaMedica.objects.filter(cedulaPaciente=paciente)
                    context['citas_medicas'] = citas_medicas

                except Paciente.DoesNotExist:
                    context['error_message'] = "Paciente no encontrado."

        except Fisioterapeuta.DoesNotExist:
            context['error_message'] = "Error: Fisioterapeuta no encontrado."
    else:
        # Verificar si la cedula del fisioterapeuta está en la sesión
        if 'fisioterapeuta_cedula' in request.session:
            fisioterapeuta_cedula = request.session['fisioterapeuta_cedula']
            return redirect('buscar_paciente', fisioterapeuta_cedula=fisioterapeuta_cedula)
        else:
            context['error_message'] = "Error: Fisioterapeuta no especificado."

    context['search_form'] = search_form
    context['cita_form'] = cita_form
    context['eliminar_cita_form'] = eliminar_cita_form
    context['agregar_terapia_form'] = agregar_terapia_form
    context['fisioterapeuta_cedula'] = fisioterapeuta_cedula
    return render(request, 'citaMedica.html', context)

# Terapias
class TerapiaView(View):
    def get(self, request):
        # Mostrar todas las terapias
        terapias = Terapia.objects.all()
        tipo_ejercicios = TipoEjercicio.objects.all()

        terapia_form = TerapiaForm()  # Formulario para crear terapia
        tipo_ejercicio_form = TipoEjercicioForm()
        ejercicio_combo_form = EjercicioComboForm() 
    
        return render(request, 'terapia_view.html', {
            'terapias': terapias,
            'terapia_form': terapia_form,
            'tipo_ejercicios': tipo_ejercicios,
            'tipo_ejercicio_form': tipo_ejercicio_form,
            'ejercicio_combo_form': ejercicio_combo_form,  # Pasa el formulario con combo box
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
            ejercicio = movimiento_form.cleaned_data.get('ejercicio')
            if ejercicio:
                movimiento.movimientoID = ejercicio
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
    
#Ejercicios####
class AgregarEjercicioAMovimientoView(View):
    def post(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)

        ejercicio_combo_form = EjercicioComboForm(request.POST)
        
        if ejercicio_combo_form.is_valid():
            tipo_ejercicio = ejercicio_combo_form.cleaned_data['tipo_ejercicio']
            Ejercicios.objects.create(
                tipoEjercicioID=tipo_ejercicio,
                movimientoID=movimiento,
                porcentaje=0  
            )
        
        return redirect('terapia_view')
    
class EliminarEjercicioView(View):
    def post(self, request, ejercicio_id):
        ejercicio = get_object_or_404(Ejercicios, pk=ejercicio_id)
        ejercicio.delete()
        return redirect('terapia_view') 