from django.shortcuts import render
from django.http import JsonResponse
from login.models import Paciente, Fisioterapeuta, CitaMedica
from .forms import BuscarPacienteForm, CitaMedicaForm
import datetime

def buscar_paciente(request):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    cita_form = CitaMedicaForm(request.POST or None)

    # Selecciona el fisioterapeuta conectado (cédula '1800000003')
    fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula='1800000003')

    if search_form.is_valid():
        cedula = search_form.cleaned_data['cedula']
        try:
            paciente = Paciente.objects.get(cedula=cedula)
            context['paciente'] = paciente

            if request.method == 'POST':
                nueva_cita = CitaMedica(
                    cedulaPaciente=paciente,
                    cedulaFisioterapeuta=fisioterapeuta_conectado,
                    fecha=datetime.date.today()  # Fecha actual
                )
                nueva_cita.save()
                context['message'] = "Cita creada exitosamente."

                # Devolver una respuesta adecuada para AJAX
                response_data = {
                    'message': "Cita creada exitosamente."
                }
                return JsonResponse(response_data)

            citas_medicas = CitaMedica.objects.filter(cedulaPaciente=paciente)
            context['citas_medicas'] = citas_medicas

        except Paciente.DoesNotExist:
            context['error_message'] = "Paciente no encontrado."

    context['search_form'] = search_form
    context['cita_form'] = cita_form
    return render(request, 'citaMedica.html', context)
