# {{CARD_ID}}: {{EPIC_TITLE}}

**Tipo:** Épico de Entrega Contratual  
**Marco Contratual Vinculado:** {{CONTRATO_MARCO_REF}} (ex: M1 - MVP Fundação)  
**Cláusula SOW de Origem:** {{SOW_CLAUSE_REF}} (ex: [ANEXO_1_SOW-SEC-4-MARCO-01])  
**Modelo de Contratação:** {{MODELO_CONTRATACAO}} (Modo A - Fixed Price / Modo B - Squad Dedicada / Modo C - Fase 0)  
**Impacto Financeiro / Faturamento:** {{PERCENTUAL_FATURAMENTO}}  
**Responsável RACI (Contratada):** {{RACI_RESPONSAVEL_CONTRATADA}}  
**Aprovador RACI (Cliente PO):** {{RACI_APROVADOR_PO_CLIENTE}}  
**Status Atual:** {{STATUS_CARD}} (DRAFT / READY / IN_PROGRESS / IN_HOMOLOGATION / ACCEPTED)

---

## 1. Visão Executiva e Escopo do Épico
{{DESCRICAO_EXECUTIVA_ESCOPO}}

### 1.1 Entregáveis Físicos em Staging Vinculados
- {{ENTREGAVEL_FISICO_1}}
- {{ENTREGAVEL_FISICO_2}}
- {{ENTREGAVEL_FISICO_3}}

### 1.2 Delimitação Taxativa de Não-Escopo (Out of Scope)
- {{NAO_ESCOPO_ITEM_1}}
- {{NAO_ESCOPO_ITEM_2}}

---

## 2. Rastreabilidade de Cards Filhos (Histórias e Enablers)
| ID do Card | Tipo | Título da História / Enabler | Story Points | Responsável | Status |
| :--- | :--- | :--- | :---: | :--- | :--- |
| {{CHILD_CARD_ID_1}} | {{CHILD_CARD_TYPE_1}} | {{CHILD_CARD_TITLE_1}} | {{CHILD_CARD_SP_1}} | {{CHILD_CARD_RESP_1}} | {{CHILD_CARD_STATUS_1}} |
| {{CHILD_CARD_ID_2}} | {{CHILD_CARD_TYPE_2}} | {{CHILD_CARD_TITLE_2}} | {{CHILD_CARD_SP_2}} | {{CHILD_CARD_RESP_2}} | {{CHILD_CARD_STATUS_2}} |

---

## 3. Critérios de Aceitação do Marco (Gate de Homologação)
1. **Implantação em Staging:** Todos os entregáveis componentes do épico devem estar implantados e com healthcheck positivo no ambiente de Staging.
2. **Homologação pelo PO:** Submissão formal ao Product Owner do Cliente para disparo do rito do Anexo 3 (Aceite Tácito em 5 dias úteis).
3. **Classificação de Inconsistências:** Ausência de falhas impeditivas classificadas como P1 (Bloqueador) ou P2 (Crítico). Falhas P3/P4 não retêm o marco.
4. **Resiliência Externa Comprovada:** Em caso de indisponibilidade de APIs legadas do Cliente, conformidade aferida via testes automatizados com mocks em CI/CD.

---

## 4. Checklist de Definition of Ready (DoR) do Épico
- [ ] Escopo substantivo aprovado e espelhado com a cláusula de faturamento do contrato.
- [ ] Dependências externas mapeadas no Anexo 2 (RACI e credenciais de Gate Zero).
- [ ] Histórias de usuário e enablers técnicos fatiados e estimados em Story Points.
- [ ] Interlocutores homologadores (PO titular e suplente) ratificados.

## 5. Checklist de Definition of Done (DoD) do Épico
- [ ] 100% dos cards filhos concluídos com DoD individual atendido.
- [ ] Suíte de testes de integração e regressão executada com 100% de sucesso.
- [ ] Relatório de conformidade NFR (latência p95 < 500ms e scans de segurança) anexado.
- [ ] Termo de Homologação formal emitido pelo PO ou transcurso formal do Aceite Tácito (5 dias úteis sem P1/P2).
- [ ] Liberação da fatura financeira correspondente ao marco contratual.
