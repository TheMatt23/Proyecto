from django import forms
from login.models import Terapia, Movimiento, TipoEjercicio, CitaMedica

class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, label="Buscar por cédula")

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['cedulaPaciente'] 

class EliminarCitaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput()) 

class AgregarTerapiaForm(forms.ModelForm):
   class Meta:
      model = Terapia
      fields = ['nombre'] 

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