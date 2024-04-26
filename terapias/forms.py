# forms.py
from django import forms
from login.models import Terapia, Movimiento, TipoEjercicio

class TerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['nombre']

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
        queryset=TipoEjercicio.objects.all(),  # Consulta para obtener los tipos de ejercicio
        empty_label="Seleccione un tipo",  # Mensaje predeterminado cuando no hay nada seleccionado
        required=True,  # Indica si este campo es obligatorio
    )