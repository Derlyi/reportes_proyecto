from django import forms

# Formulario para seleccionar fechas
class SalesReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de inicio")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de fin")
