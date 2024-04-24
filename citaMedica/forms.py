from django import forms
from login.models import Paciente, CitaMedica

class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, label="Buscar por cédula")
