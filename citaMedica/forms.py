from django import forms
from login.models import CitaMedica,Terapia

class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, label="Buscar por cédula")

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['cedulaPaciente'] 

class EliminarCitaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput()) 


class TerapiaForm(forms.Form):
    cita_id = forms.IntegerField(widget=forms.HiddenInput())

class AgregarTerapiaForm(forms.ModelForm):
   class Meta:
      model = Terapia
      fields = ['nombre'] 

class EliminarTerapiaForm(forms.Form):
    terapia_id = forms.IntegerField()