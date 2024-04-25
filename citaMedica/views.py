from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from login.models import Paciente, Fisioterapeuta, CitaMedica, Terapia, Movimiento, CitaMedica
from .forms import BuscarPacienteForm, CitaMedicaForm, AgregarTerapiaForm, EliminarCitaForm
import datetime


def buscar_paciente(request):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    cita_form = CitaMedicaForm(request.POST or None)
    eliminar_cita_form = EliminarCitaForm(request.POST or None)
    agregar_terapia_form = AgregarTerapiaForm(request.POST or None)

    fisioterapeuta_conectado = Fisioterapeuta.objects.get(cedula='1800000003')

    if search_form.is_valid():
        cedula = search_form.cleaned_data['cedula']
        try:
            paciente = Paciente.objects.get(cedula=cedula)
            context['paciente'] = paciente

            if request.method == 'POST':

                if 'crear_cita' in request.POST:
                    nueva_cita = CitaMedica(
                        cedulaPaciente=paciente,
                        cedulaFisioterapeuta=fisioterapeuta_conectado,
                        fecha=datetime.date.today()  # Fecha actual
                    )
                    nueva_cita.save()

                if 'eliminar_cita' in request.POST and eliminar_cita_form.is_valid():
                    cita_id = eliminar_cita_form.cleaned_data['cita_id']
                    CitaMedica.objects.filter(pk=cita_id).delete()

                if 'agregar_terapia' in request.POST and agregar_terapia_form.is_valid():
                    cita_id = request.POST.get("cita_id")  # Asegúrate de obtener el cita_id
                    return redirect('', cita_id=cita_id)
                
            citas_medicas = CitaMedica.objects.filter(cedulaPaciente=paciente)
            context['citas_medicas'] = citas_medicas

        except Paciente.DoesNotExist:
            context['error_message'] = "Paciente no encontrado."

    context['search_form'] = search_form
    context['cita_form'] = cita_form
    context['eliminar_cita_form'] = eliminar_cita_form
    context['agregar_terapia_form'] = agregar_terapia_form
    return render(request, 'citaMedica.html', context)