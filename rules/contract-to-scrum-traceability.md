---
description: Padrão normativo de rastreabilidade bidirecional, taxonomia, particionamento granular e governança anti-vazamento de escopo entre contratos e cards ágeis.
trigger: model_decision
---

# DIRETRIZES DE RASTREABILIDADE E TAXONOMIA CONTRATUAL EM CARDS ÁGEIS

As diretrizes deste documento regem a fidelidade absoluta entre os anexos técnicos do contrato (`ANEXO_1_SOW`, `ANEXO_2_RACI`, `ANEXO_3_HOMOLOGACAO`, `ANEXO_4_CHANGE_REQUEST`, `ANEXO_5_GARANTIA_SLA`) e o catálogo de cards ágeis gerados pela esteira de engenharia.

---

## 1. Princípios Fundamentais de Rastreabilidade

### 1.1 Invariante de Cobertura Contratual Total (Zero Scope Leakage)
- Toda e qualquer obrigação técnica, entregável funcional, premissa de integração, pré-requisito de ambiente e rito de homologação estipulados nos anexos do contrato deve possuir pelo menos 1 (um) card correspondente no backlog.
- O auditor de qualidade (`scrum-quality-auditor`) deve aferir que nenhum item do SOW ou dos demais anexos permaneceu órfão ou desprovido de materialização ágil.

### 1.2 Invariante Anti-Gold-Plating (Zero Scope Creep)
- É terminantemente vedada a criação de cards contendo escopo funcional ou técnico não previsto, explícita ou implicitamente, nos anexos contratuais aprovados.
- Funcionalidades "adicionais", "melhorias sugeridas" ou desejos não pactuados identificados durante a decomposição devem ser obrigatoriamente isolados como **Candidatos a Change Request (CR)**, formatados conforme o Anexo 4, e nunca incorporados ao backlog base da contratação.

---

## 2. Taxonomia e Sistema de Numeração de Cards

A decomposição deve adotar prefixos padronizados e numeração determinística, garantindo rápida identificação em issue trackers (Jira, GitHub Issues, Linear, Azure DevOps):

| Prefixo | Camada / Tipo de Card | Diretório Destino | Origem Primária no Contrato |
| :--- | :--- | :--- | :--- |
| `GZ-XXX` | Pré-Requisito de Gate Zero | `00_GATE_ZERO/` | Anexo 2 (Seção 3 - Marco Zero) |
| `EPIC-XX` | Épico / Marco de Entrega | `01_EPICS/` | Anexo 1 (Seção 4 - Marcos M0..Mn) |
| `US-XXXX` | História de Usuário Funcional | `02_USER_STORIES/` | Anexo 1 (Seção 3 - Escopo Substantivado) |
| `ENABLER-XXXX` | Enabler Técnico / Spike / NFR | `03_TECHNICAL_ENABLERS/` | Anexo 1 (Seções 2 e 5 - Stack, NFRs e Premissas) |
| `QA-XXXX` | Protocolo de Homologação / UAT | `04_QA_ACCEPTANCE/` | Anexo 3 (Protocolo de Aceite, P1-P4 e Reteste) |
| `GOV-XXXX` | Salvaguarda de Governança e SLA | `05_GOVERNANCE_SAFEGUARDS/` | Anexo 2 (RACI/LGPD) e Anexo 5 (Garantia/SLA) |

---

## 3. Particionamento Físico e Granularidade (Anti-Inchaço de Arquivo Único)

- **Proibição de Arquivo Único Monolítico:** A geração do backlog ágil não pode ser concentrada em um único arquivo `.md` gigante. Essa prática inviabiliza revisões por múltiplos desenvolvedores, gera conflitos de merge e prejudica a importação em ferramentas de gestão de projetos.
- **Estrutura Obrigatória de Pastas:** Os cards devem ser gerados como arquivos `.md` individuais, agrupados tematicamente nas seguintes pastas dentro do diretório de saída:
  ```
  backlog/
  ├── INDEX_BACKLOG_TAXONOMY.md
  ├── 00_GATE_ZERO/
  │   ├── GZ-001-LIBERACAO-ACESSOS-AMBIENTES.md
  │   └── GZ-002-SETUP-CI-CD-MOCK-SANDBOX.md
  ├── 01_EPICS/
  │   ├── EPIC-01-FUNDACAO-ARQUITETURAL.md
  │   └── EPIC-02-[NOME_DO_MODULO].md
  ├── 02_USER_STORIES/
  │   ├── US-0101-[NOME_DA_HISTORIA].md
  │   └── US-0102-[NOME_DA_HISTORIA].md
  ├── 03_TECHNICAL_ENABLERS/
  │   ├── ENABLER-0101-INTEGRACAO-API-LATENCIA.md
  │   └── ENABLER-0102-MIGRATION-SCHEMA-BANCO.md
  ├── 04_QA_ACCEPTANCE/
  │   ├── QA-0101-PLANO-HOMOLOGACAO-STAGING.md
  │   └── QA-0102-SUITE-MOCK-RESILIENCIA-LEGADO.md
  └── 05_GOVERNANCE_SAFEGUARDS/
      ├── GOV-001-CONFORMIDADE-LGPD-DADOS-SINTETICOS.md
      ├── GOV-002-MONITORAMENTO-SLA-RESPOSTA-FREEZE.md
      └── GOV-003-RITO-GARANTIA-SUPORTE-SLA.md
  ```

---

## 4. Matriz de Rastreabilidade Bidirecional

O arquivo `INDEX_BACKLOG_TAXONOMY.md` deve conter a tabela de rastreabilidade consolidando a relação:
`[Cláusula Contratual] <---> [ID do Card] <---> [Arquivo Físico] <---> [Responsável RACI] <---> [Status DoR/DoD]`.

Essa matriz constitui o artefato de auditoria jurídica e técnica primário que comprova que cada real orçado no contrato possui entrega de engenharia correspondente e verificável.
