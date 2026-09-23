# Relatório de Implementação – Entrega P1
**Disciplina:** Laboratório de Programação Full Stack  
**Professor:** Márcio Garrido  
**Projeto:** Agenda de Consultas  

## Descrição das Features Implementadas

Na **Feature 1 (Busca e Filtro na Listagem)**, foi implementada na página principal de profissionais a busca textual pelo nome do profissional e um filtro condicional por sua especialidade. A escolha dessas variáveis justifica-se por serem os principais parâmetros utilizados na rotina de recepção para localizar médicos e especialistas de forma rápida[cite: 1]. O formulário preserva o termo buscado na URL via `request.GET.get()`, mantendo o estado do campo preenchido no template[cite: 1].

Na **Feature 2 (Validação Customizada no Formulário)**, foi adicionada uma regra de negócio no `ModelForm` (`forms.py`) para **impedir a seleção de datas no passado** no agendamento de consultas[cite: 1]. Essa regra de domínio garante a integridade dos dados no banco de dados[cite: 1], evitando inconsistências operacionais e agendamentos retroativos no sistema.