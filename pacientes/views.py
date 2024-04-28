from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.models import Paciente, Terapia

@login_required
def paciente_detalle(request):
    cedula_paciente = request.user.cedula  # Obtiene la cédula del paciente autenticado

    paciente = Paciente.objects.get(cedula=cedula_paciente)
    terapias = Terapia.objects.filter(cedulaPaciente=paciente)
    terapias_info = []

    for terapia in terapias:
        # Procesa cada terapia como desees
        terapias_info.append({
            'id': terapia.id,
            'fisioterapeuta_nombre': terapia.fisioterapeuta.nombre,
            'fisioterapeuta_apellido': terapia.fisioterapeuta.apellido,
            'nombre_terapia': terapia.nombre,
            'fecha_terapia': terapia.fecha.strftime('%d/%m/%Y') if terapia.fecha else ''
        })

    return render(request, 'pacientesDetalle.html', {'paciente': paciente, 'terapias_info': terapias_info})
