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
    Ejercicio,
    MovimientosEjercicios,
    Resultados
)

# Configuración personalizada para Admin
class AdminAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar en el listado
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar
    list_filter = ('celular',)  # Agrega un filtro por celular

# Configuración personalizada para Paciente
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar en el listado
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar
    list_filter = ('celular',)  # Agrega un filtro por celular

# Configuración personalizada para Fisioterapeuta
class FisioterapeutaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'celular')  # Campos a mostrar en el listado
    search_fields = ('cedula', 'nombre', 'apellido')  # Campos por los que se puede buscar
    list_filter = ('celular',)  # Agrega un filtro por celular

# Configuración personalizada para TipoLesion
class TipoLesionAdmin(admin.ModelAdmin):
    list_display = ('lesionID', 'nombreLesion')  # Campos a mostrar en el listado
    search_fields = ('nombreLesion',)  # Campos por los que se puede buscar

# Configuración personalizada para HistorialPaciente
class HistorialPacienteAdmin(admin.ModelAdmin):
    list_display = ('historialID', 'cedulaPaciente', 'lesionID')  # Campos a mostrar en el listado
    search_fields = ('cedulaPaciente', 'lesionID')  # Campos por los que se puede buscar

# Configuración personalizada para CitaMedica
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ('citaID', 'cedulaFisioterapeuta', 'cedulaPaciente', 'fecha')  # Campos a mostrar
    search_fields = ('cedulaFisioterapeuta', 'cedulaPaciente')  # Campos por los que se puede buscar
    list_filter = ('fecha',)  # Filtro por fecha

# Configuración personalizada para Terapia
class TerapiaAdmin(admin.ModelAdmin):
    list_display = ('terapiaID', 'citaID', 'nombre', 'fecha')  # Campos a mostrar
    search_fields = ('nombre',)  # Campo por el que se puede buscar
    list_filter = ('fecha',)  # Filtro por fecha

# Configuración personalizada para Movimiento
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('movimientoID', 'terapiaID', 'nombre')  # Campos a mostrar
    search_fields = ('nombre',)  # Campo por el que se puede buscar

# Configuración personalizada para TipoEjercicio
class TipoEjercicioAdmin(admin.ModelAdmin):
    list_display = ('tipoEjercicioID', 'nombre', 'url')  # Campos a mostrar
    search_fields = ('nombre',)  # Campo por el que se puede buscar

# Configuración personalizada para Ejercicio
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('ejercicioID', 'tipoEjercicioID')  # Campos a mostrar
    search_fields = ('tipoEjercicioID',)  # Campo por el que se puede buscar

# Configuración para MovimientosEjercicios
class MovimientosEjerciciosAdmin(admin.ModelAdmin):
    list_display = ('movimientoID', 'ejercicioID', 'porcentaje')  # Campos a mostrar
    list_filter = ('porcentaje',)  # Filtro por porcentaje

# Configuración para Resultados
class ResultadosAdmin(admin.ModelAdmin):
    list_display = ('resultadoID', 'movimientoID', 'cantidadPos', 'cantidadNeg', 'porcentaje')  # Campos a mostrar
    list_filter = ('porcentaje',)  # Filtro por porcentaje

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
admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(MovimientosEjercicios, MovimientosEjerciciosAdmin)
admin.site.register(Resultados, ResultadosAdmin)
