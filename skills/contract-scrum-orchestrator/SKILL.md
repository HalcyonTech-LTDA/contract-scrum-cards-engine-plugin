---
name: contract-scrum-orchestrator
description: >-
  Orquestra a esteira agêntica (Staged Multi-Agent DAG) de engenharia para transformar os anexos técnicos do contrato
  (SOW, RACI, Homologação, CR e SLA) em um backlog ágil profissional particionado em cards modulares (Epics, Stories,
  Enablers, QA e Salvaguardas), com rastreabilidade total, Definition of Ready (DoR) e Definition of Done (DoD).
---

# Contract Scrum Orchestrator Skill

Esta skill expõe o comando `/contract-scrum-orchestrator` e instrui o modelo orquestrador a coordenar a esteira agêntica nativa para transformar anexos técnicos contratuais em um catálogo completo e profissional de cards ágeis em Markdown, com estrita granularidade, hierarquia bem definida e ausência de arquivos monolíticos inchados.

A inteligência de coordenação reside nas instruções deste documento: o modelo orquestrador avalia os parâmetros de entrada, executa o pre-flight check, injeta os templates da pasta local da skill, coordena os agentes especialistas em Fan-Out paralelo e aciona a auditoria cruzada em Fan-In (Generator-Critic).

---

## Gatilhos e Invocação
- **Comando direto via Slash Command:** `/contract-scrum-orchestrator [caminho_anexos_ou_dossie] [diretorio_saida]`
- **Invocação contextual por linguagem natural:** Sempre que o usuário solicitar:
  - Decompor anexos técnicos contratuais ou minutas contratuais em cards ágeis, histórias de usuário ou épicos;
  - Gerar backlog do Jira / GitHub Projects / Linear com DoR e DoD a partir do SOW, RACI ou Protocolo de Homologação;
  - Mapear rastreabilidade técnica entre cláusulas contratuais e backlog de engenharia.

---

## Estrutura Física e Isolamento de Handoff
- **Localização dos Templates da Skill:** Os templates estruturais residem obrigatoriamente em:
  `skills/contract-scrum-orchestrator/templates/`
  - `EPIC.template.md`
  - `USER_STORY.template.md`
  - `TECHNICAL_ENABLER.template.md`
  - `QA_HOMOLOGATION.template.md`
  - `GATE_ZERO_SAFEGUARD.template.md`
  - `INDEX_BACKLOG_TAXONOMY.template.md`
- **Isolamento de Handoff Transitório:** O artefato intermediário de dados deve ser salvo exclusivamente em `{{output_dir}}/.scratch/normalized_backlog_baseline.json`. A pasta `.scratch/` é ignorada pelo controle de versão (`.gitignore`), garantindo um diretório final de entrega limpo e auditável.
- **Higienização Estrita de Saída (.md):** Todos os agentes redatores e o auditor são instruídos a remover integralmente qualquer comentário HTML (`<!-- ... -->`) e garantir que nenhum placeholder `{{...}}` permaneça nos cards finais.

---

## Fluxo de Execução Obrigatório (DAG Multi-Agente)

```
[Anexos Técnicos / ANEXO_TECNICO_MESTRE_CONTRATO.md]
                       │
                       ▼ (Passo 1: Sequencial com Pre-Flight Check)
        [annexes-ingestion-normalizer]
                       │
                       ▼
    [{{output_dir}}/.scratch/normalized_backlog_baseline.json]
                       │
   ┌───────────────────┼───────────────────┬───────────────────┐
   │ (Passo 2: Fan-Out Paralelo por Especialistas de Domínio)   │
   ▼                   ▼                   ▼                   ▼
[po-backlog]     [arch-enabler]        [qa-homol]         [gov-safeguard]
   │                   │                   │                   │
   ▼                   ▼                   ▼                   ▼
01_EPICS/        03_TECHNICAL_       04_QA_              00_GATE_ZERO/
02_USER_STORIES/     ENABLERS/           ACCEPTANCE/     05_GOVERNANCE_
   │                   │                   │                   │
   └───────────────────┼───────────────────┴───────────────────┘
                       │
                       ▼ (Passo 3: Fan-In & Generator-Critic Reflexion)
             [scrum-quality-auditor]
                       │
                       ▼
       [{{output_dir}}/INDEX_BACKLOG_TAXONOMY.md]
```

### Passo 1: Ingestão e Pre-Flight Check (Sequencial)
1. Identifique o caminho dos anexos de entrada:
   - Se for informado um diretório (ex: `./anexos_contratuais`), o normalizador busca `ANEXO_TECNICO_MESTRE_CONTRATO.md` ou os arquivos `ANEXO_1_SOW.md` a `ANEXO_5_GARANTIA_SLA.md`.
   - Se for informado um arquivo específico, o normalizador lê diretamente este arquivo.
   - Diretório de saída padrão: `./backlog` (ou o caminho especificado pelo usuário). Crie a pasta `{{output_dir}}/.scratch/`.
2. Acione o subagente `annexes-ingestion-normalizer`.
3. **Avaliação da Barreira de Qualidade:**
   - **Bloqueio Estrito (`STATUS: BLOCKED_MISSING_PRECONDITIONS`):** Interrompa se faltarem o escopo funcional essencial ou a definição da stack tecnológica.
   - **Fallbacks Padrão:** Injeta defaults contratuais (janela de 5 dias úteis de homologação em Staging, 2 dias de reteste, 16h úteis de SLA de resposta, garantia técnica de 60 dias) e registra em `applied_defaults`.
4. O normalizador grava a baseline canônica em `{{output_dir}}/.scratch/normalized_backlog_baseline.json`.

### Passo 2: Decomposição Especializada dos Cards (Fan-Out Paralelo)
Com a baseline validada em `.scratch/`, acione simultaneamente os 4 agentes especialistas, injetando seus respectivos templates:

1. **`po-backlog-decomposer`**:
   - Cria a pasta `{{output_dir}}/01_EPICS/` e gera os cards `EPIC-XX-[NOME].md` para cada marco/módulo contratual.
   - Cria a pasta `{{output_dir}}/02_USER_STORIES/` e gera os cards `US-XXXX-[NOME].md` para cada entregável funcional.
   - Aplica critérios INVEST, formatação canônica de persona, critérios BDD/Gherkin (mínimo 2 cenários), rastreabilidade contratual `[SOW-SEC-X]` e checklists de DoR e DoD.

2. **`architecture-enabler-decomposer`**:
   - Cria a pasta `{{output_dir}}/03_TECHNICAL_ENABLERS/` e gera os cards `ENABLER-XXXX-[NOME].md`.
   - Cobre fundação da stack, schemas de banco/migrações, contratos OpenAPI/Swagger, meta de latência p95 < 500ms, simuladores/mocks para isolamento de quedas de legados do Cliente e esteira CI/CD com 80% de cobertura.

3. **`qa-homologation-decomposer`**:
   - Cria a pasta `{{output_dir}}/04_QA_ACCEPTANCE/` e gera os cards `QA-XXXX-[NOME].md`.
   - Estrutura o roteiro de homologação em Staging, rastreando cenários BDD das histórias, taxonomia binária P1-P4, template dos 5 requisitos de evidência técnica, rito de Aceite Tácito em 5 dias úteis e janela estrita de reteste de até 2 dias úteis.

4. **`governance-safeguard-decomposer`**:
   - Cria a pasta `{{output_dir}}/00_GATE_ZERO/` e gera os cards de pré-requisitos: `GZ-001-LIBERACAO-ACESSOS-AMBIENTES.md` e `GZ-002-SETUP-CI-CD-MOCK-SANDBOX.md`.
   - Cria a pasta `{{output_dir}}/05_GOVERNANCE_SAFEGUARDS/` e gera os cards: `GOV-001` (LGPD e dados sintéticos), `GOV-002` (SLA de resposta de 16h úteis e Schedule Freeze), `GOV-003` (Governança formal de Change Requests) e `GOV-004` (Garantia de 60 dias e SLA de suporte).

### Passo 3: Auditoria Cruzada e Compilação do Backlog (Fan-In / Generator-Critic)
1. Acione o subagente `scrum-quality-auditor` fornecendo a baseline JSON e todos os cards gerados nos subdiretórios de saída.
2. O auditor inspeciona 100% dos cards quanto a:
   - Cobertura contratual total (Zero Scope Leakage);
   - Ausência de escopo adicional não contratado (Zero Scope Creep);
   - Conformidade estrita com as regras normativas de DoR e DoD;
   - Granularidade adequada (teto de 8 Story Points por história);
   - Higienização de comentários HTML e eliminação de placeholders expostos.
3. Se algum card violar os padrões, o auditor aciona o loop de **Reflexion**, determinando o ajuste pontual antes da homologação final.
4. Compila o documento mestre **`{{output_dir}}/INDEX_BACKLOG_TAXONOMY.md`**, consolidando o Quadro Sinóptico de Governança, métricas totais de esforço (Story Points) e a **Matriz de Rastreabilidade Bidirecional**.

---

## Entrega Final ao Usuário
Apresente no chat:
1. Resumo executivo do backlog gerado com métricas consolidadas (Épicos, Histórias, Enablers, QA suites, Salvaguardas e Story Points totais).
2. Tabela de rastreabilidade e quadro sinóptico de governança com destaque para os defaults aplicados.
3. Confirmação do particionamento físico das pastas e arquivos gerados em disco.
4. Confirmação de higienização dos arquivos gerados.
