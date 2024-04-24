from django.shortcuts import render, redirect, get_object_or_404
from login.models import Paciente, Fisioterapeuta, CitaMedica
from .forms import BuscarPacienteForm
import datetime
from django import forms


class CitaMedicaForm(forms.Form):
    fisioterapeuta = forms.ModelChoiceField(queryset=Fisioterapeuta.objects.all(), label="Fisioterapeuta")

# Simulación del fisioterapeuta conectado
#fisioterapeuta = Fisioterapeuta.objects.get(cedula='1800000003')  # Fisioterapeuta simulado

def buscar_paciente(request):
    context = {}
    search_form = BuscarPacienteForm(request.GET or None)
    cita_form = CitaMedicaForm(request.POST or None)

    if search_form.is_valid():
        cedula = search_form.cleaned_data['cedula']
        try:
            paciente = Paciente.objects.get(cedula=cedula)
            context['paciente'] = paciente

            if request.method == 'POST' and cita_form.is_valid():
                fisioterapeuta = cita_form.cleaned_data['fisioterapeuta']
                nueva_cita = CitaMedica(
                    cedulaPaciente=paciente,
                    cedulaFisioterapeuta=fisioterapeuta,
                    fecha=datetime.date.today()
                )
                nueva_cita.save()
                context['message'] = "Cita creada exitosamente."
                return redirect('buscar_paciente')  # Redirigir para evitar múltiples envíos

            citas_medicas = CitaMedica.objects.filter(cedulaPaciente=paciente)
            context['citas_medicas'] = citas_medicas

        except Paciente.DoesNotExist:
            context['error_message'] = "Paciente no encontrado."

    context['search_form'] = search_form
    context['cita_form'] = cita_form
    return render(request, 'citaMedica.html', context)