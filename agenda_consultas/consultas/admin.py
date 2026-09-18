from django.contrib import admin
from .models import Paciente, Profissional, Disponibilidade, Consulta


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ("usuario", "especialidade")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "telefone")


@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ("profissional", "data", "hora_inicio", "hora_fim")
    list_filter = ("profissional",)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "profissional", "data", "hora_inicio", "hora_fim", "status")
    list_filter = ("status", "profissional")
