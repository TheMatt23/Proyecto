from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.models import Paciente, Terapia, Resultados
from django.db.models import Sum
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot
from django.shortcuts import redirect
from login.views import pantalla_inicio as login_pantalla_inicio
from django.contrib.auth import logout

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

def cerrar_sesion(request):
    logout(request)
    return login_pantalla_inicio(request)

def ver_reporte(request, terapia_id):
    # Consulta para obtener los valores positivos y negativos de la tabla Resultados
    resultados = Resultados.objects.filter(movimientoID__terapiaID=terapia_id).aggregate(
        total_positivo=Sum('cantidadPos'),
        total_negativo=Sum('cantidadNeg')
    )

    # Datos del gráfico
    labels = ['Cantidad Positiva', 'Cantidad Negativa']
    valores = [resultados['total_positivo'] or 0, resultados['total_negativo'] or 0]

    # Crear el gráfico
    data = [
        go.Bar(
            x=labels,
            y=valores,
            marker=dict(color=['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)']),
            opacity=0.8
        )
    ]

    layout = go.Layout(
        title='Reporte Gráfico',
        xaxis=dict(title='Categorías'),
        yaxis=dict(title='Cantidad')
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'reporteGrafico.html', {'plot_div': plot_div})

def reporte_general(request):
     # Obtener la cédula del paciente de la sesión
    cedula_paciente = request.session.get('cedula_paciente')

    if cedula_paciente:
        # Buscar al paciente por su cédula
        paciente = Paciente.objects.get(cedula=cedula_paciente)

        # Obtener todas las terapias asociadas al paciente
        terapias = Terapia.objects.filter(cedulaPaciente=paciente)

        # Inicializar listas para almacenar los resultados de cada terapia
        resultados_positivos = []
        resultados_negativos = []

        for terapia in terapias:
            # Consultar los resultados para cada terapia y sumar los valores positivos y negativos
            resultados = Resultados.objects.filter(movimientoID__terapiaID=terapia.terapiaID).aggregate(
                total_positivo=Sum('cantidadPos'),
                total_negativo=Sum('cantidadNeg')
            )

            # Agregar los resultados a las listas
            resultados_positivos.append(resultados['total_positivo'] or 0)
            resultados_negativos.append(resultados['total_negativo'] or 0)

        # Crear el gráfico
        data = [
            go.Bar(
                x=['Terapia {}'.format(i + 1) for i in range(len(terapias))],
                y=resultados_positivos,
                name='Cantidad Positiva',
                marker=dict(color='rgba(75, 192, 192, 0.2)'),
                opacity=0.8
            ),
            go.Bar(
                x=['Terapia {}'.format(i + 1) for i in range(len(terapias))],
                y=resultados_negativos,
                name='Cantidad Negativa',
                marker=dict(color='rgba(255, 99, 132, 0.2)'),
                opacity=0.8
            )
        ]

        layout = go.Layout(
            title='Reporte Gráfico General',
            xaxis=dict(title='Terapias'),
            yaxis=dict(title='Cantidad'),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return render(request, 'reporteGeneral.html', {'plot_div': plot_div, 'paciente': paciente})
    else:
        # Manejar el caso si no se encuentra la cédula del paciente en la sesión
        return redirect('login')
    
    
    