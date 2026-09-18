# Agenda de Consultas — P1

Projeto 2 do catálogo: **Agenda de Consultas**, com agendamento validando a
disponibilidade real do profissional.

## Entidades → Modelos

| Entidade do catálogo | Onde está no código |
|---|---|
| paciente | `Paciente` (perfil ligado a um `User`) |
| profissional | `Profissional` (perfil ligado a um `User`) |
| disponibilidade | `Disponibilidade` (bloco de data + hora_inicio + hora_fim) |
| consulta | `Consulta` |

## Regra de negócio (P1)

Em `consultas/models.py`, `Consulta.clean()` só deixa a consulta ser salva se:

1. o horário pedido (`hora_inicio`–`hora_fim`) estiver **totalmente contido**
   em algum bloco de `Disponibilidade` cadastrado pelo profissional naquela
   data; **e**
2. não houver **conflito** com outra consulta já agendada para o mesmo
   profissional no mesmo horário.

Esse `clean()` é chamado automaticamente pelo Django quando o `ConsultaForm`
é validado (`form.is_valid()`), então tanto a interface web quanto o admin
respeitam a regra. Se falhar, a mensagem de erro aparece no formulário.

## Perfis (paciente / profissional)

Não há sistema de papéis/permissões ainda (isso é do P2) — no cadastro, a
pessoa simplesmente escolhe se é "Paciente" ou "Profissional" e o app cria o
perfil correspondente. A tela inicial (`home`) muda de acordo com o perfil:
profissionais veem suas disponibilidades e agenda; pacientes veem a lista de
profissionais para marcar e suas próprias consultas.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # opcional, para acessar /admin/

python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Crie uma conta como "Profissional",
cadastre disponibilidades; depois crie outra conta como "Paciente" (em uma
aba anônima, por exemplo) e tente marcar uma consulta dentro e fora dos
horários disponíveis para ver a validação funcionando.

## O que fica para o P2 (não incluído aqui)

- Múltiplas clínicas
- Papéis de usuário (admin, recepção, etc.)
- Dashboard com métricas
- API REST com Django REST Framework (DRF)
