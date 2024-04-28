from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.models import Paciente, Terapia

from django.shortcuts import redirect

@login_required
def paciente_detalle(request):
    cedula_paciente = request.session.get('cedula_paciente')  # Obtiene la cédula del paciente de la sesión

    if cedula_paciente:
        paciente = Paciente.objects.get(cedula=cedula_paciente)
        terapias = Terapia.objects.filter(cedulaPaciente=paciente)
        terapias_info = []

        for terapia in terapias:
            # Procesa cada terapia como desees
            terapias_info.append({
                'id': terapia.terapiaID,
                'nombre_terapia': terapia.nombre,
                'fecha_terapia': terapia.fecha.strftime('%d/%m/%Y') if terapia.fecha else ''
            })

        return render(request, 'pacientesPantalla.html', {'paciente': paciente, 'terapias_info': terapias_info})
    else:
        # Redirige al usuario a otra vista si no se encuentra la cédula del paciente en la sesión
        return redirect('login')  # Reemplaza 'otra_vista' con el nombre de la vista a la que quieres redirigir al usuario

