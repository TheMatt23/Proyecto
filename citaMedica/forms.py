from django import forms
from login.models import Terapia, Movimiento, TipoEjercicio, Paciente, HistorialPaciente, TipoLesion
from django.forms import inlineformset_factory

# Crea un formulario para registrar información básica del paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula', 'nombre', 'apellido', 'celular', 'direccion', 'contrasena']

# Crea un formulario para registrar el historial del paciente, permitiendo agregar lesiones
class HistorialPacienteForm(forms.ModelForm):
    # Añadimos un campo para seleccionar el tipo de lesión
    lesionID = forms.ModelChoiceField(queryset=TipoLesion.objects.all(), required=True, label='Tipo de Lesión')

    class Meta:
        model = HistorialPaciente
        fields = ['lesionID']

HistorialFormSet = inlineformset_factory(
    Paciente,
    HistorialPaciente,
    form=HistorialPacienteForm,
    extra=1,  # Puedes ajustar para agregar más lesiones por defecto
    can_delete=False,  # Deshabilitar opción de eliminación
)




#################################3
class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, label="Buscar por cédula")

class EliminarCitaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput()) 

class AgregarTerapiaForm(forms.ModelForm):
   class Meta:
      model = Terapia
      fields = ['nombre'] 

###################################################
#Terapias

# forms.py
class TerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['nombre', 'fecha']

# Formulario para agregar movimientos
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['nombre'] 

# Tipo Ejercico
class TipoEjercicioForm(forms.ModelForm):
    class Meta:
        model = TipoEjercicio
        fields = ['nombre', 'url']

class EjercicioComboForm(forms.Form):
    tipo_ejercicio = forms.ModelChoiceField(
        queryset=TipoEjercicio.objects.all(), 
        empty_label="Seleccione un tipo",
        required=True, 
    )
