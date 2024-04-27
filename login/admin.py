from django.contrib import admin
from .models import (
    Admin,
    Paciente,
    Fisioterapeuta,
    TipoLesion,
    HistorialPaciente,
    CitaMedica,
    Terapia,
    Movimiento,
    TipoEjercicio,
    Ejercicios,
    Resultados,
    AsignarTerapias
)

# Configuración personalizada para Admin
class AdminAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar en el listado
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar

# Configuración personalizada para Paciente
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar

# Configuración personalizada para Fisioterapeuta
class FisioterapeutaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar

# Configuración personalizada para TipoLesion
class TipoLesionAdmin(admin.ModelAdmin):
    list_display = ('lesionID', 'nombreLesion')  # Campos a mostrar
    search_fields = ('nombreLesion',)  # Campos por los que se puede buscar

# Configuración personalizada para HistorialPaciente
class HistorialPacienteAdmin(admin.ModelAdmin):
    list_display = ('historialID', 'cedulaPaciente', 'lesionID')  # Campos a mostrar
    search_fields = ('cedulaPaciente_cedula', 'lesionID_nombreLesion')  # Campos para búsqueda por relaciones

# Configuración personalizada para CitaMedica
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ('citaID', 'cedulaFisioterapeuta', 'cedulaPaciente', 'fecha')  # Campos a mostrar
    search_fields = ('cedulaFisioterapeuta_cedula', 'cedulaPaciente_cedula')  # Campos por los que se puede buscar
    list_filter = ('fecha',)  # Filtro por fecha

# Configuración personalizada para Terapia
class TerapiaAdmin(admin.ModelAdmin):
    list_display = ('terapiaID', 'nombre', 'fecha')  # Campos a mostrar
    search_fields = ('nombre',)  # Campo por el que se puede buscar

# Configuración personalizada para Movimiento
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('movimientoID', 'terapiaID', 'nombre')  # Campos a mostrar
    search_fields = ('nombre', 'terapiaID__nombre')  # Campo por el que se puede buscar
    list_filter = ('terapiaID',)  # Filtro por terapia

# Configuración personalizada para TipoEjercicio
class TipoEjercicioAdmin(admin.ModelAdmin):
    list_display = ('tipoEjercicioID', 'nombre', 'url')  # Campos a mostrar
    search_fields = ('nombre',)  # Campo por el que se puede buscar

# Configuración personalizada para Ejercicio
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('ejercicioID', 'tipoEjercicioID')  # Campos a mostrar
    search_fields = ('tipoEjercicioID__nombre',)  # Campo por el que se puede buscar

# Configuración para Resultados
class ResultadosAdmin(admin.ModelAdmin):
    list_display = ('resultadoID', 'movimientoID', 'cantidadPos', 'cantidadNeg', 'porcentaje')  # Campos a mostrar
    list_filter = ('porcentaje',)  # Filtro por porcentaje

# Configuración para AsignarTerapias
class AsignarTerapiasAdmin(admin.ModelAdmin):
    list_display = ('AgigID', 'citaID', 'terapiaID', 'fecha')  # Campos a mostrar
    search_fields = ('citaID_citaID', 'terapiaID_nombre')  # Campos por los que se puede buscar

# Registrar los modelos y sus configuraciones personalizadas
admin.site.register(Admin, AdminAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Fisioterapeuta, FisioterapeutaAdmin)
admin.site.register(TipoLesion, TipoLesionAdmin)
admin.site.register(HistorialPaciente, HistorialPacienteAdmin)
admin.site.register(CitaMedica, CitaMedicaAdmin)
admin.site.register(Terapia, TerapiaAdmin)
admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(TipoEjercicio, TipoEjercicioAdmin)
admin.site.register(Ejercicios, EjercicioAdmin)
admin.site.register(Resultados, ResultadosAdmin)
admin.site.register(AsignarTerapias, AsignarTerapiasAdmin) 