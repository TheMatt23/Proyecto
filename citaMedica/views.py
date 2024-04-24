from django.shortcuts import render, redirect
from login.models import Paciente, Fisioterapeuta, CitaMedica
from .forms import BuscarPacienteForm, CitaMedicaForm

def generar_cita(request):
    fisioterapeuta = Fisioterapeuta.objects.get(cedula='1800000003')  # Fisioterapeuta simulado
    paciente = None
    buscar_form = BuscarPacienteForm()
    cita_form = CitaMedicaForm()

    if request.method == 'POST':
        if 'buscar_paciente' in request.POST:
            # Buscar al paciente por cédula
            buscar_form = BuscarPacienteForm(request.POST)
            if buscar_form.is_valid():
                cedula = buscar_form.cleaned_data['cedula']
                paciente = Paciente.objects.filter(cedula=cedula).first()

                if paciente:
                    # Redefine el formulario para crear la cita con el paciente encontrado
                    cita_form = CitaMedicaForm(initial={'cedulaPaciente': paciente})
                else:
                    # Paciente no encontrado, muestra un mensaje de error
                    return render(request, 'citaMedica.html', {
                        'buscar_form': buscar_form,
                        'cita_form': cita_form,
                        'error': "No se encontró un paciente con esta cédula. Inténtelo de nuevo.",
                    })

        elif 'generar_cita' in request.POST:
            cita_form = CitaMedicaForm(request.POST)
            if cita_form.is_valid():
                # Antes de guardar, verifica que se haya asignado un paciente
                paciente = cita_form.cleaned_data['cedulaPaciente']
                if paciente:
                    nueva_cita = cita_form.save(commit=False)
                    nueva_cita.cedulaFisioterapeuta = fisioterapeuta  # Fisioterapeuta simulado
                    nueva_cita.cedulaPaciente = paciente  # Paciente encontrado
                    nueva_cita.save()  # Guarda la cita médica
                    return redirect('exito')  # Redirige a la página de éxito

    # Página inicial o cuando hay errores
    return render(request, 'citaMedica.html', {
        'buscar_form': buscar_form,
        'cita_form': cita_form,
        'paciente': paciente,
    })

def exito(request):
    return render(request, 'exito.html') 