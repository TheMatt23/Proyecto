from django.shortcuts import render, redirect
from .forms import PacienteForm, HistorialFormSet

# Vista para registrar pacientes y añadir lesiones a su historial en un solo paso
def registrar_paciente(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)  # formulario del paciente
        formset = HistorialFormSet(request.POST, instance=paciente_form.instance)  # formulario para lesiones

        if paciente_form.is_valid() and formset.is_valid():
            # Guarda el paciente primero
            nuevo_paciente = paciente_form.save()

            # Guarda el formset de lesiones, asociándolo al paciente recién creado
            formset.instance = nuevo_paciente
            formset.save()

            return redirect('//')  # Redirige después de guardar con éxito

    else:
        paciente_form = PacienteForm()  # formulario vacío para paciente
        formset = HistorialFormSet()  # formset vacío para lesiones

    return render(request, 'registrarPaciente.html', {
        'paciente_form': paciente_form,
        'formset': formset,
    })
