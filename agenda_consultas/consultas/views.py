from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CadastroForm, ConsultaForm, DisponibilidadeForm
from .models import Consulta, Disponibilidade, Paciente, Profissional


def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data["tipo"] == "profissional":
                Profissional.objects.create(
                    usuario=user, especialidade=form.cleaned_data.get("especialidade", "")
                )
            else:
                Paciente.objects.create(usuario=user)
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect("home")
    else:
        form = CadastroForm()
    return render(request, "consultas/cadastro.html", {"form": form})


def _perfil(request):
    """Retorna ('profissional', obj) ou ('paciente', obj) para o usuário logado."""
    if hasattr(request.user, "perfil_profissional"):
        return "profissional", request.user.perfil_profissional
    if hasattr(request.user, "perfil_paciente"):
        return "paciente", request.user.perfil_paciente
    return None, None


@login_required
def home(request):
    tipo, perfil = _perfil(request)
    if tipo == "profissional":
        disponibilidades = perfil.disponibilidades.all()
        consultas = perfil.consultas.exclude(status=Consulta.STATUS_CANCELADA)
        return render(
            request,
            "consultas/home_profissional.html",
            {"perfil": perfil, "disponibilidades": disponibilidades, "consultas": consultas},
        )
    elif tipo == "paciente":
        consultas = perfil.consultas.exclude(status=Consulta.STATUS_CANCELADA)
        return render(request, "consultas/home_paciente.html", {"perfil": perfil, "consultas": consultas})
    else:
        messages.error(request, "Sua conta não tem um perfil de paciente ou profissional associado.")
        return render(request, "consultas/home_paciente.html", {"perfil": None, "consultas": []})


@login_required
def disponibilidade_create(request):
    tipo, perfil = _perfil(request)
    if tipo != "profissional":
        messages.error(request, "Apenas profissionais podem cadastrar disponibilidade.")
        return redirect("home")

    if request.method == "POST":
        disponibilidade = Disponibilidade(profissional=perfil)
        form = DisponibilidadeForm(request.POST, instance=disponibilidade)
        if form.is_valid():
            form.save()
            messages.success(request, "Disponibilidade cadastrada!")
            return redirect("home")
    else:
        form = DisponibilidadeForm()
    return render(request, "consultas/disponibilidade_form.html", {"form": form})


@login_required
def disponibilidade_delete(request, pk):
    tipo, perfil = _perfil(request)
    disponibilidade = get_object_or_404(Disponibilidade, pk=pk, profissional=perfil)
    if request.method == "POST":
        disponibilidade.delete()
        messages.success(request, "Disponibilidade removida.")
    return redirect("home")


@login_required
def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, "consultas/profissional_list.html", {"profissionais": profissionais})


@login_required
def consulta_create(request, profissional_pk):
    tipo, perfil = _perfil(request)
    if tipo != "paciente":
        messages.error(request, "Apenas pacientes podem marcar consultas.")
        return redirect("home")

    profissional = get_object_or_404(Profissional, pk=profissional_pk)

    if request.method == "POST":
        consulta = Consulta(paciente=perfil, profissional=profissional)
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta agendada com sucesso!")
            return redirect("home")
    else:
        form = ConsultaForm()

    return render(
        request,
        "consultas/consulta_form.html",
        {"form": form, "profissional": profissional},
    )


@login_required
def consulta_cancelar(request, pk):
    tipo, perfil = _perfil(request)
    consulta = get_object_or_404(Consulta, pk=pk)
    dono = (tipo == "paciente" and consulta.paciente_id == perfil.id) or (
        tipo == "profissional" and consulta.profissional_id == perfil.id
    )
    if not dono:
        messages.error(request, "Você não pode cancelar esta consulta.")
        return redirect("home")

    if request.method == "POST":
        consulta.cancelar()
        messages.info(request, "Consulta cancelada.")
    return redirect("home")


@login_required
def consulta_realizar(request, pk):
    tipo, perfil = _perfil(request)
    consulta = get_object_or_404(Consulta, pk=pk, profissional=perfil)
    if tipo != "profissional":
        messages.error(request, "Apenas o profissional pode marcar a consulta como realizada.")
        return redirect("home")
    if request.method == "POST":
        consulta.marcar_realizada()
        messages.success(request, "Consulta marcada como realizada.")
    return redirect("home")
