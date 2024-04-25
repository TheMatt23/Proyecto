from django import forms
from login.models import CitaMedica,Terapia, Movimiento, Ejercicio

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


class AgregarTerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['nombre', 'cantidadTerapias']  # Puedes agregar más campos si los necesitas

class EliminarTerapiaForm(forms.Form):
    terapia_id = forms.IntegerField()

class AgregarMovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['nombre']  # Puedes agregar más campos si los necesitas

class EliminarMovimientoForm(forms.Form):
    movimiento_id = forms.IntegerField()

class AgregarEjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['tipoEjercicioID']  # Puedes agregar más campos si los necesitas

class EliminarEjercicioForm(forms.Form):
    ejercicio_id = forms.IntegerField()