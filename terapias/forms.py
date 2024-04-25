# forms.py
from django import forms
from login.models import Terapia, Movimiento

class TerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['nombre']

# Formulario para agregar movimientos
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['nombre'] 
