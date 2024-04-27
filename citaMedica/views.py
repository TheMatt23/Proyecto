from django.shortcuts import render, redirect
from django.http import JsonResponse
from login.models import Paciente, Fisioterapeuta
from .forms import BuscarPacienteForm, AgregarTerapiaForm, EliminarCitaForm
import datetime

def buscar_paciente(request, fisioterapeuta_cedula=None):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    eliminar_cita_form = EliminarCitaForm(request.POST or None)
    agregar_terapia_form = AgregarTerapiaForm(request.POST or None)

    if fisioterapeuta_cedula:
        try:
            # Obtener el fisioterapeuta conectado
            fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula=fisioterapeuta_cedula)

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
