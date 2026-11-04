# {{CARD_ID}}: {{STORY_TITLE}}

**Tipo:** História de Usuário (User Story)  
**Épico Pai:** {{PARENT_EPIC_REF}}  
**Cláusula SOW de Origem:** {{SOW_CLAUSE_REF}} (ex: [ANEXO_1_SOW-SEC-3.1-ITEM-02])  
**Estimativa:** {{STORY_POINTS}} Story Points  
**Prioridade de Negócio:** {{PRIORITY}} (Alta / Média / Baixa)  
**Responsável Técnico (Squad):** {{TECH_ASSIGNEE}}  
**Homologador Exclusivo (Cliente PO):** {{CLIENT_PO}}  
**Status Atual:** {{STATUS_CARD}} (BACKLOG / READY / IN_PROGRESS / IN_REVIEW / IN_HOMOLOGATION / DONE)

---

## 1. Narrativa da História (User Persona Framing)

- **Como** {{USER_PERSONA}}
- **Quero** {{ACTION_AND_CAPABILITY}}
- **Para que** {{MEASURABLE_BUSINESS_BENEFIT}}

---

## 2. Escopo Funcional Detalhado e Regras de Negócio

### 2.1 Regras de Negócio Substantivas
1. {{BUSINESS_RULE_1}}
2. {{BUSINESS_RULE_2}}
3. {{BUSINESS_RULE_3}}

### 2.2 Delimitação de Não-Escopo desta História
- {{OUT_OF_SCOPE_ITEM_1}}
- {{OUT_OF_SCOPE_ITEM_2}}

---

## 3. Critérios de Aceitação em BDD / Gherkin

```gherkin
Cenário: {{GHERKIN_SCENARIO_1_TITLE}}
  Dado que {{GHERKIN_SCENARIO_1_GIVEN}}
  Quando {{GHERKIN_SCENARIO_1_WHEN}}
  Então {{GHERKIN_SCENARIO_1_THEN}}

Cenário: {{GHERKIN_SCENARIO_2_TITLE}}
  Dado que {{GHERKIN_SCENARIO_2_GIVEN}}
  Quando {{GHERKIN_SCENARIO_2_WHEN}}
  Então {{GHERKIN_SCENARIO_2_THEN}}
```

---

## 4. Premissas Técnicas e Integrações
- **Contratos de API / OpenAPI:** `{{OPENAPI_SPEC_REFERENCE}}`
- **Tabelas / Entidades de Dados:** `{{DATABASE_ENTITIES}}`
- **Premissa de Latência Contratual:** Tempo de resposta p95 inferior a 500ms em todas as rotas vinculadas.
- **Ambiente de Testes:** Homologação exclusiva em Staging com dados sintéticos/anonimizados (LGPD).

---

## 5. Checklist de Definition of Ready (DoR)
- [ ] Rastreabilidade formal com a cláusula do contrato (`{{SOW_CLAUSE_REF}}`) explicitada.
- [ ] Narrativa substantiva sem verbos ambíguos.
- [ ] Mínimo de 2 cenários BDD/Gherkin estruturados (caminho feliz e tratamento de exceção).
- [ ] Pré-requisitos técnicos, contratos de API e modelos de dados mapeados.
- [ ] Não-escopo claramente delimitado.
- [ ] Estimativa aprovada pela Squad em até 8 Story Points.
- [ ] PO homologador do Cliente identificado e ciente da janela de 5 dias úteis de Staging.

## 6. Checklist de Definition of Done (DoD)
- [ ] Código-fonte implementado conforme boas práticas e linter aprovado sem alertas críticos.
- [ ] Testes unitários com cobertura mínima de 80% das ramificações.
- [ ] Testes de integração automatizados validados no pipeline de CI/CD.
- [ ] Premissa de latência p95 < 500ms validada em Staging.
- [ ] Conformidade LGPD: ausência total de dados pessoais reais (PII) de produção no ambiente.
- [ ] Pull Request revisado e aprovado pelo Tech Lead.
- [ ] Deploy executado com sucesso no ambiente de Staging.
- [ ] Pacote de evidências técnicas anexado para homologação do PO do Cliente.
