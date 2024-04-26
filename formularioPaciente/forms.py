from django import forms
from django.forms import inlineformset_factory
from login.models import Paciente, HistorialPaciente, TipoLesion


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

# Configuración del formset para añadir múltiples lesiones asociadas a un paciente
HistorialFormSet = inlineformset_factory(
    Paciente,
    HistorialPaciente,
    form=HistorialPacienteForm,
    extra=1,  # Puedes ajustar para agregar más lesiones por defecto
    can_delete=False,  # Deshabilitar opción de eliminación
)
