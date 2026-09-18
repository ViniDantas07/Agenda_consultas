from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Consulta, Disponibilidade


class CadastroForm(UserCreationForm):
    TIPO_CHOICES = [
        ("paciente", "Paciente"),
        ("profissional", "Profissional"),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.RadioSelect)
    especialidade = forms.CharField(
        required=False, help_text="Preencha apenas se você for profissional."
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class DisponibilidadeForm(forms.ModelForm):
    class Meta:
        model = Disponibilidade
        fields = ["data", "hora_inicio", "hora_fim"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["data", "hora_inicio", "hora_fim", "observacoes"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
