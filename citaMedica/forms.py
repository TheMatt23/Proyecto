from django import forms
from login.models import CitaMedica

class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, label="Buscar por cédula")

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['cedulaPaciente'] 

class EliminarCitaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput()) 

class AgregarTerapiaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput())