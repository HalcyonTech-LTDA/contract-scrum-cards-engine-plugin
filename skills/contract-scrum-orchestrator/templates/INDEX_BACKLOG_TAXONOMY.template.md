# ÍNDICE GERAL DO BACKLOG E MATRIZ DE RASTREABILIDADE CONTRATUAL

**Projeto:** {{PROJETO_NOME}}  
**Contratante (Cliente):** {{CLIENTE_NOME}} (Controlador LGPD)  
**Contratada:** {{CONTRATADA_NOME}} (Operadora Técnica LGPD)  
**Modelo de Contratação:** {{MODELO_CONTRATACAO}}  
**Contrato / Documento Mestre de Referência:** {{CONTRATO_MESTRE_REF}}  
**Data da Decomposição do Backlog:** {{DATA_GERACAO}}  
**Status do Gate Zero:** {{GATE_ZERO_OVERALL_STATUS}} (PENDING_SIGNATURE / CLEARED)

---

## 1. Quadro Sinóptico de Governança do Backlog Ágil

| Parâmetro de Governança Contratual | Valor / Rito Estabelecido no Contrato | Aplicação Operacional nos Cards |
| :--- | :--- | :--- |
| **Modelo Comercial de Execução** | {{MODELO_CONTRATACAO}} | Estruturação de Épicos por Marcos M0..Mn ou Sprints |
| **Gate Zero / Marco Zero** | Termo de Liberação Integral de Acessos assinado | Cards em `00_GATE_ZERO/` bloqueiam avanço funcional |
| **SLA de Resposta do Cliente** | Até 2 dias úteis de expediente comercial (16h úteis) | Atrasos disparam congelamento 1:1 (*Schedule Freeze*) |
| **Desmobilização / Remobilização** | Atraso > 10 dias úteis gera realocação (5 dias remobilização) | Aplicável taxa de Standby Fee da Squad retida |
| **Homologação em Staging** | 5 (cinco) dias úteis com **Janela de Reteste de até 2 dias úteis** | Cards em `04_QA_ACCEPTANCE/` com rito de Aceite Tácito |
| **Severidades P1 a P4** | Apenas P1/P2 retêm faturamento; P3/P4 não retêm | Classificação binária em todos os cards de teste |
| **Resiliência a Quedas de Legados** | Indisponibilidade de APIs externas não pausa homologação | Mocks e stubs em `03_TECHNICAL_ENABLERS/` |
| **Privacidade de Dados (LGPD)** | Vedação de dados de produção em Dev/Staging | Dados sintéticos obrigatórios em todas as histórias |
| **Governança de Mudanças (CR)** | Nulidade de canais informais; decisão em 3 dias | Solicitações fora do SOW isoladas como Change Request |
| **Garantia Técnica e Suporte** | 60 dias do Aceite/Go-Live; suporte 09h-18h dias úteis | Cards de governança em `05_GOVERNANCE_SAFEGUARDS/` |

---

## 2. Métricas Consolidadas do Backlog

- **Total de Épicos Contratuais (`01_EPICS/`):** {{TOTAL_EPICS_COUNT}}
- **Total de Histórias de Usuário (`02_USER_STORIES/`):** {{TOTAL_STORIES_COUNT}}
- **Total de Enablers Técnicos e Spikes (`03_TECHNICAL_ENABLERS/`):** {{TOTAL_ENABLERS_COUNT}}
- **Total de Suítes de Homologação QA (`04_QA_ACCEPTANCE/`):** {{TOTAL_QA_COUNT}}
- **Total de Cards de Gate Zero e Salvaguardas (`00_GATE_ZERO/` e `05_GOVERNANCE_SAFEGUARDS/`):** {{TOTAL_SAFEGUARDS_COUNT}}
- **Esforço Total Estimado:** {{TOTAL_STORY_POINTS}} Story Points

---

## 3. Matriz de Rastreabilidade Bidirecional (Contrato <-> Cards)

A tabela abaixo estabelece o vínculo auditável entre cada dispositivo dos anexos contratuais e sua materialização técnica no backlog:

| Cláusula Contratual de Origem | ID do Card | Camada / Tipo | Título do Card | Caminho do Arquivo Físico | Status DoR | Status DoD |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
{{TABELA_RASTREABILIDADE_LINHAS}}

---

## 4. Diretrizes de Consumo do Backlog pela Squad

1. **Importação nos Issue Trackers:** A estrutura particionada de pastas e arquivos `.md` individuais permite a importação direta via scripts automatizados ou CLI para Jira, GitHub Projects, Linear ou Azure DevOps.
2. **Prioridade de Execução:**
   - **Fase 1:** Conclusão obrigatória dos cards de `00_GATE_ZERO/`. Nenhum card funcional pode ser iniciado antes da assinatura do Termo de Liberação Integral de Acessos.
   - **Fase 2:** Implementação dos Enablers Técnicos fundamentais (`03_TECHNICAL_ENABLERS/`) para assegurar conformidade com NFRs (latência < 500ms) e mocks de resiliência.
   - **Fase 3:** Execução das Histórias de Usuário (`02_USER_STORIES/`) por marcos de entrega.
   - **Fase 4:** Execução dos ritos de homologação (`04_QA_ACCEPTANCE/`) em Staging, com disparo do Aceite Tácito em 5 dias úteis.
   - **Fase 5:** Monitoramento contínuo das Salvaguardas (`05_GOVERNANCE_SAFEGUARDS/`).
