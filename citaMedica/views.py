from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from login.models import Paciente, Fisioterapeuta, CitaMedica
from .forms import BuscarPacienteForm, CitaMedicaForm

def generar_cita(request):
    fisioterapeuta = Fisioterapeuta.objects.get(cedula='1800000003')  # Fisioterapeuta simulado
    paciente = None  # Paciente inicial
    citas = []  # Lista de citas asociadas al paciente
    buscar_form = BuscarPacienteForm()  # Formulario para buscar
    cita_form = CitaMedicaForm()  # Formulario para agregar citas

    if request.method == 'POST':
        if 'buscar_paciente' in request.POST:
            buscar_form = BuscarPacienteForm(request.POST)
            if buscar_form.is_valid():
                cedula = buscar_form.cleaned_data['cedula']
                paciente = Paciente.objects.filter(cedula=cedula).first()

                if paciente:
                    # Obtener citas del paciente
                    citas = CitaMedica.objects.filter(cedulaPaciente=paciente)

        elif 'agregar_cita' in request.POST:
            if paciente is None:
                # Si no hay paciente, muestra un error
                return HttpResponseBadRequest("Debe buscar y seleccionar un paciente antes de agregar una cita.")

            # Agregar una cita médica para el paciente seleccionado
            cita_form = CitaMedicaForm(request.POST)
            if cita_form.is_valid():
                nueva_cita = cita_form.save(commit=False)
                nueva_cita.cedulaFisioterapeuta = fisioterapeuta  # Fisioterapeuta simulado
                nueva_cita.cedulaPaciente = paciente  # Paciente seleccionado
                nueva_cita.save()  # Guarda la cita
                return redirect(request.path_info)  # Recargar para limpiar el formulario

        elif 'limpiar' in request.POST:
            # Limpiar los formularios
            buscar_form = BuscarPacienteForm()  # Limpiar el formulario de búsqueda
            cita_form = CitaMedicaForm()  # Limpiar el formulario de cita
            citas = []  # Limpiar las citas asociadas
            paciente = None  # Limpiar el paciente seleccionado

    return render(request, 'citaMedica.html', {
        'buscar_form': buscar_form,
        'cita_form': cita_form,
        'paciente': paciente,
        'citas': citas,
    })
