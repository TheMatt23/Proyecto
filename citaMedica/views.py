from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from login.models import Paciente, Fisioterapeuta, CitaMedica, Terapia, Movimiento, CitaMedica
from .forms import BuscarPacienteForm, CitaMedicaForm, AgregarTerapiaForm, EliminarCitaForm, TerapiaForm

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
