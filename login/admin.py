from django.contrib import admin
from .models import Admin, Paciente, Fisioterapeuta, TipoLesion, HistorialPaciente, Terapia, Movimiento, TipoEjercicio, Ejercicios, AsignarTerapias, Resultados

# Register your models here.

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'celular', 'direccion']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'celular', 'direccion']

@admin.register(Fisioterapeuta)
class FisioterapeutaAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'celular', 'direccion']

@admin.register(TipoLesion)
class TipoLesionAdmin(admin.ModelAdmin):
    list_display = ['lesionID', 'nombreLesion']

@admin.register(HistorialPaciente)
class HistorialPacienteAdmin(admin.ModelAdmin):
    list_display = ['historialID', 'cedulaPaciente', 'lesionID']

@admin.register(Terapia)
class TerapiaAdmin(admin.ModelAdmin):
    list_display = ['terapiaID', 'cedulaFisioterapeuta', 'cedulaPaciente', 'nombre', 'fecha']

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['movimientoID', 'terapiaID', 'nombre']

@admin.register(TipoEjercicio)
class TipoEjercicioAdmin(admin.ModelAdmin):
    list_display = ['tipoEjercicioID', 'nombre', 'url']

@admin.register(Ejercicios)
class EjerciciosAdmin(admin.ModelAdmin):
    list_display = ['ejercicioID', 'tipoEjercicioID', 'movimientoID', 'porcentaje']

@admin.register(AsignarTerapias)
class AsignarTerapiasAdmin(admin.ModelAdmin):
    list_display = ['AgigID', 'terapiaID', 'fecha']

@admin.register(Resultados)
class ResultadosAdmin(admin.ModelAdmin):
    list_display = ['resultadoID', 'movimientoID', 'cantidadPos', 'cantidadNeg', 'porcentaje']
