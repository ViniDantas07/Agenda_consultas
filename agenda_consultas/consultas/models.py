from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Profissional(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_profissional"
    )
    especialidade = models.CharField(max_length=100, blank=True)

    def __str__(self):
        nome = self.usuario.get_full_name() or self.usuario.username
        return f"{nome} ({self.especialidade})" if self.especialidade else nome


class Paciente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_paciente"
    )
    telefone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Disponibilidade(models.Model):
    """Bloco de horário em que o profissional aceita marcações."""

    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="disponibilidades"
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        ordering = ["data", "hora_inicio"]

    def __str__(self):
        return f"{self.data} {self.hora_inicio}–{self.hora_fim}"

    def clean(self):
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError("O horário de início deve ser antes do horário de término.")


class Consulta(models.Model):
    STATUS_AGENDADA = "agendada"
    STATUS_CANCELADA = "cancelada"
    STATUS_REALIZADA = "realizada"
    STATUS_CHOICES = [
        (STATUS_AGENDADA, "Agendada"),
        (STATUS_CANCELADA, "Cancelada"),
        (STATUS_REALIZADA, "Realizada"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name="consultas")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AGENDADA)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data", "hora_inicio"]

    def __str__(self):
        return f"{self.paciente} com {self.profissional} em {self.data} {self.hora_inicio}"

    def clean(self):
        """
        Regra central do P1: o agendamento só é válido se cair dentro de um
        bloco de disponibilidade do profissional E não conflitar com outra
        consulta já marcada (disponibilidade REAL, não só a cadastrada).
        """
        if not (self.data and self.hora_inicio and self.hora_fim and self.profissional_id):
            return

        if self.hora_inicio >= self.hora_fim:
            raise ValidationError("O horário de início deve ser antes do horário de término.")

        dentro_da_disponibilidade = self.profissional.disponibilidades.filter(
            data=self.data,
            hora_inicio__lte=self.hora_inicio,
            hora_fim__gte=self.hora_fim,
        ).exists()
        if not dentro_da_disponibilidade:
            raise ValidationError(
                "O profissional não tem disponibilidade cadastrada para esse dia/horário."
            )

        conflitos = (
            Consulta.objects.filter(
                profissional=self.profissional,
                data=self.data,
                status=self.STATUS_AGENDADA,
            )
            .exclude(pk=self.pk)
            .filter(hora_inicio__lt=self.hora_fim, hora_fim__gt=self.hora_inicio)
        )
        if conflitos.exists():
            raise ValidationError(
                "Já existe uma consulta marcada para este profissional nesse horário."
            )

    def cancelar(self):
        self.status = self.STATUS_CANCELADA
        self.save()

    def marcar_realizada(self):
        self.status = self.STATUS_REALIZADA
        self.save()
