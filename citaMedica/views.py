from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from login.models import Paciente, Fisioterapeuta, Terapia, TipoEjercicio, Movimiento, Ejercicios, Resultados
from .forms import PacienteForm, HistorialFormSet, BuscarPacienteForm, AgregarTerapiaForm, EliminarCitaForm, TerapiaForm, TerapiaForm, MovimientoForm, TipoEjercicioForm, EjercicioComboForm
from django.db import transaction 
import plotly.graph_objs as go
from django.db.models import Sum
from plotly.offline import plot


#Pacientes
def registrar_paciente(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)  # formulario del paciente
        formset = HistorialFormSet(request.POST, instance=paciente_form.instance)  # formulario para lesiones

        if paciente_form.is_valid() and formset.is_valid():
            nuevo_paciente = paciente_form.save()

            formset.instance = nuevo_paciente
            formset.save()

            return redirect('')  

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
                    return JsonResponse({'message': 'Cita eliminada exitosamente.'})  # Respuesta para AJAX

                if 'agregar_terapia' in request.POST and agregar_terapia_form.is_valid():
                    return JsonResponse({'message': 'Terapia agregada exitosamente.'})  # Respuesta para AJAX

            if search_form.is_valid():
                cedula = search_form.cleaned_data['cedula']
                try:
                    paciente = Paciente.objects.get(cedula=cedula)
                    context['paciente'] = paciente

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
        paciente_cedula = paciente.cedula
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
            'ejercicio_combo_form': ejercicio_combo_form
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
        paciente = terapia.cedulaPaciente
        terapia.delete()  # Eliminar la terapia
        return redirect('terapia_view', cedula=paciente.cedula)  
    
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

#############################
class TipoEjercicioDeleteView(View):
    def post(self, request, tipo_ejercicio_id):
        tipo_ejercicio = get_object_or_404(TipoEjercicio, pk=tipo_ejercicio_id)
        tipo_ejercicio.delete()  # Elimina el tipo de ejercicio

        return HttpResponse(status=204)
      


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

class ActualizarPorcentajeView(View):
    def post(self, request):
        ejercicio_id = request.POST.get('ejercicio_id')
        # Obtiene el ejercicio a partir del ID pasado en el formulario
        ejercicio = get_object_or_404(Ejercicios, pk=ejercicio_id)
        terapia = ejercicio.movimientoID.terapiaID  # Acceder a la terapia a través del movimiento
        paciente = terapia.cedulaPaciente  # Obtener la cédula del paciente asociado
        
        nuevo_porcentaje = float(request.POST.get('porcentaje'))

        ejercicio.porcentaje = nuevo_porcentaje  # Actualiza el porcentaje
        ejercicio.save()  # Guarda el cambio en la base de datos

        #terapia = ejercicio.movimientoID.terapiaID
        
        actualizar_resultados(terapia)

        # Redirigir a una vista relevante
        return redirect('terapia_view', cedula=paciente.cedula)
    

####Actulizar los porcentajes
def calcular_ejercicios_positivos_negativos(terapia):
    # Obtener todos los movimientos asociados con la terapia
    movimientos = Movimiento.objects.filter(terapiaID=terapia)

    # Obtener todos los ejercicios relacionados con esos movimientos
    ejercicios = Ejercicios.objects.filter(movimientoID__in=movimientos)

    # Contar ejercicios positivos y negativos
    cantidad_positivos = sum(1 for ejercicio in ejercicios if ejercicio.porcentaje >= 70)
    cantidad_negativos = sum(1 for ejercicio in ejercicios if ejercicio.porcentaje < 70)

    return cantidad_positivos, cantidad_negativos

def actualizar_resultados(terapia):
    cantidad_positivos, cantidad_negativos = calcular_ejercicios_positivos_negativos(terapia)

    with transaction.atomic():  # Para garantizar consistencia
        # Obtener o crear el resultado para esta terapia
        resultado, created = Resultados.objects.get_or_create(terapiaID=terapia)
        resultado.cantidadPos = cantidad_positivos
        resultado.cantidadNeg = cantidad_negativos
        resultado.save()  # Guardar cambios
    

def cargar_resultados_terapia(request, terapia_id):
    terapia = get_object_or_404(Terapia, terapiaID=terapia_id)
    resultados = terapia.resultados_set.all()  # Obtener resultados asociados con la terapia

    contexto = {
        'terapia': terapia,
        'resultados': resultados,
    }

    return render(request, 'terapia_view.html', contexto)


#####
def ver_reporte(request, terapia_id):
    # Consulta para obtener los valores positivos y negativos de la tabla Resultados
    resultados = Resultados.objects.filter(terapiaID=terapia_id).aggregate(
        total_positivo=Sum('cantidadPos'),
        total_negativo=Sum('cantidadNeg')
    )

    # Datos del gráfico
    labels = ['Correctos', 'Incorrectos']
    valores = [resultados['total_positivo'] or 0, resultados['total_negativo'] or 0]

    # Crear el gráfico
    data = [
        go.Bar(
            x=labels,
            y=valores,
            marker=dict(color=['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)']),
            opacity=0.8
        )
    ]

    layout = go.Layout(
        title='Reporte Terapia',
        xaxis=dict(title='Movimientos'),
        yaxis=dict(title='Ejercicios')
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'reporteGrafico.html', {'plot_div': plot_div})

