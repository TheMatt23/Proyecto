from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from login.models import Paciente, Fisioterapeuta, Terapia, TipoEjercicio, Movimiento, Ejercicios
from .forms import PacienteForm, HistorialFormSet, BuscarPacienteForm, AgregarTerapiaForm, EliminarCitaForm, TerapiaForm, TerapiaForm, MovimientoForm, TipoEjercicioForm, EjercicioComboForm


#Pacientes
def registrar_paciente(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)  # formulario del paciente
        formset = HistorialFormSet(request.POST, instance=paciente_form.instance)  # formulario para lesiones

        if paciente_form.is_valid() and formset.is_valid():
            nuevo_paciente = paciente_form.save()

            # Guarda el formset de lesiones, asociándolo al paciente recién creado
            formset.instance = nuevo_paciente
            formset.save()

            return redirect('')  # Redirige después de guardar con éxito

    else:
        paciente_form = PacienteForm()  # formulario vacío para paciente
        formset = HistorialFormSet()  # formset vacío para lesiones

    return render(request, 'registrarPaciente.html', {
        'paciente_form': paciente_form,
        'formset': formset,
    })

#Vista Home
def buscar_paciente(request, fisioterapeuta_cedula=None):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    eliminar_cita_form = EliminarCitaForm(request.POST or None)
    agregar_terapia_form = AgregarTerapiaForm(request.POST or None)

    if fisioterapeuta_cedula:
        try:
            fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula=fisioterapeuta_cedula)
            request.session['fisioterapeuta_cedula'] = fisioterapeuta_conectado.cedula

            if request.method == 'POST':
                if 'eliminar_cita' in request.POST and eliminar_cita_form.is_valid():
                    cita_id = eliminar_cita_form.cleaned_data['cita_id']
                    # Eliminar la cita (o la terapia asociada)
                    # Aquí deberías escribir el código para eliminar la cita o la terapia asociada según tu lógica
                    return JsonResponse({'message': 'Cita eliminada exitosamente.'})  # Respuesta para AJAX

                if 'agregar_terapia' in request.POST and agregar_terapia_form.is_valid():
                    # Aquí deberías escribir el código para agregar la terapia según tu lógica
                    return JsonResponse({'message': 'Terapia agregada exitosamente.'})  # Respuesta para AJAX

            if search_form.is_valid():
                cedula = search_form.cleaned_data['cedula']
                try:
                    paciente = Paciente.objects.get(cedula=cedula)
                    context['paciente'] = paciente

                    # Aquí deberías obtener las terapias asociadas al paciente según tu lógica
                    # terapias = Terapia.objects.filter(...)  # Escribe tu filtro aquí
                    # context['terapias'] = terapias

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
    context['eliminar_cita_form'] = eliminar_cita_form
    context['agregar_terapia_form'] = agregar_terapia_form
    context['fisioterapeuta_cedula'] = fisioterapeuta_cedula
    return render(request, 'citaMedica.html', context)

# Terapias
class TerapiaView(View):
    def get(self, request, cedula):
        paciente = Paciente.objects.get(cedula=cedula) 
        terapias = Terapia.objects.filter(cedulaPaciente=paciente)
        fisioterapeuta_cedula = request.session.get('fisioterapeuta_cedula')

        if fisioterapeuta_cedula:
            fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula=fisioterapeuta_cedula)

        tipo_ejercicios = TipoEjercicio.objects.all()

        terapia_form = TerapiaForm()  # Formulario para crear terapia
        tipo_ejercicio_form = TipoEjercicioForm()
        ejercicio_combo_form = EjercicioComboForm() 
    
        return render(request, 'terapia_view.html', {
            'paciente': paciente,
            'fisioterapeuta': fisioterapeuta_conectado,
            'terapias': terapias,
            'terapia_form': terapia_form,
            'tipo_ejercicios': tipo_ejercicios,
            'tipo_ejercicio_form': tipo_ejercicio_form,
            'ejercicio_combo_form': ejercicio_combo_form,
        })


    def post(self, request, cedula):

        fisioterapeuta_cedula = request.session.get('fisioterapeuta_cedula')
        fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula=fisioterapeuta_cedula)
        paciente = Paciente.objects.get(cedula=cedula)

        if 'add_terapia' in request.POST:
            terapia_form = TerapiaForm(request.POST)
            if terapia_form.is_valid():
                nueva_terapia = terapia_form.save(commit=False)  # No guardar aún
                nueva_terapia.cedulaFisioterapeuta = fisioterapeuta_conectado
                nueva_terapia.cedulaPaciente = paciente  # Agregar paciente al modelo
                nueva_terapia.save()

        elif 'add_tipo_ejercicio' in request.POST:
            tipo_ejercicio_form = TipoEjercicioForm(request.POST)
            if tipo_ejercicio_form.is_valid():
                tipo_ejercicio_form.save()  # Guarda el nuevo tipo de ejercicio
        
        return redirect('terapia_view', cedula=cedula)  
    
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

        paciente = terapia.cedulaPaciente  # Asegúrate de obtener la cédula del paciente
        return redirect('terapia_view', cedula=paciente.cedula)  # Redirige a la misma página

# Vista para eliminar movimientos
class MovimientoDeleteView(View):
    def post(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
        terapia = movimiento.terapiaID  
        movimiento.delete() 
        
        paciente = terapia.cedulaPaciente  # Obtener el paciente asociado a la terapia
        return redirect('terapia_view', cedula=paciente.cedula)

class TipoEjercicioDeleteView(View):
    def post(self, request, tipo_ejercicio_id):
        tipo_ejercicio = get_object_or_404(TipoEjercicio, pk=tipo_ejercicio_id)
        tipo_ejercicio.delete()  # Elimina el tipo de ejercicio
        return redirect('terapia_view') 
    
#Ejercicios####
class AgregarEjercicioAMovimientoView(View):
    def post(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
        terapia = movimiento.terapiaID  
        paciente = terapia.cedulaPaciente 

        ejercicio_combo_form = EjercicioComboForm(request.POST)
        
        if ejercicio_combo_form.is_valid():
            tipo_ejercicio = ejercicio_combo_form.cleaned_data['tipo_ejercicio']
            Ejercicios.objects.create(
                tipoEjercicioID=tipo_ejercicio,
                movimientoID=movimiento,
                porcentaje=0  
            )
        
        return redirect('terapia_view', cedula=paciente.cedula)  # Proporcionar la cédula del paciente
    
class EliminarEjercicioView(View):
    def post(self, request, ejercicio_id):
        ejercicio = get_object_or_404(Ejercicios, pk=ejercicio_id)
        terapia = ejercicio.movimientoID.terapiaID  # Acceder a la terapia a través del movimiento
        paciente = terapia.cedulaPaciente  # Obtener la cédula del paciente asociado

        ejercicio.delete()
        return redirect('terapia_view', cedula=paciente.cedula)  # Pasar el argumento requerido
