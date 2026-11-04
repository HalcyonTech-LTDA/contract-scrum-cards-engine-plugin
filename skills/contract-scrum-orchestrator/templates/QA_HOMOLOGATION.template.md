# {{CARD_ID}}: {{QA_TITLE}}

**Tipo:** Protocolo e Roteiro de Homologação / Aceite Técnico (UAT)  
**Marco / Épico Vinculado:** {{TARGET_EPIC_REF}}  
**Cláusula Contratual de Origem:** {{HOMOLOGATION_CLAUSE_REF}} (ex: [ANEXO_3_PROTOCOLO_HOMOLOGACAO-SEC-1])  
**Ambiente Exclusivo de Testes:** Staging  
**Janela de Homologação:** 5 (cinco) dias úteis contados da notificação formal de entrega  
**Janela Estrita de Reteste:** Até 2 (dois) dias úteis adstrita exclusivamente ao apontamento corrigido  
**Líder de QA (Contratada):** {{QA_LEAD_ASSIGNEE}}  
**Product Owner Homologador (Cliente):** {{CLIENT_PO_EVALUATOR}}  
**Status Atual:** {{STATUS_CARD}} (PLANNED / STAGING_DEPLOYED / IN_EVALUATION / DEEMED_ACCEPTED / SIGNED_OFF)

---

## 1. Escopo do Rito de Homologação em Staging
{{HOMOLOGATION_SCOPE_DESCRIPTION}}

---

## 2. Matriz de Cenários de Teste e Rastreabilidade
| ID do Cenário | História Vinculada | Tipo (Manual / E2E Automatizado) | Pré-condições | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{TEST_CASE_ID_1}} | {{TEST_CASE_STORY_1}} | {{TEST_CASE_TYPE_1}} | {{TEST_CASE_PRECOND_1}} | {{TEST_CASE_EXPECTED_1}} | {{TEST_CASE_STATUS_1}} |
| {{TEST_CASE_ID_2}} | {{TEST_CASE_STORY_2}} | {{TEST_CASE_TYPE_2}} | {{TEST_CASE_PRECOND_2}} | {{TEST_CASE_EXPECTED_2}} | {{TEST_CASE_STATUS_2}} |

---

## 3. Matriz de Classificação Binária de Severidade (Anexo 3)
Em conformidade estrita com o Protocolo de Homologação contratual:

- **Severidade P1 (Bloqueador) ou P2 (Crítico sem contorno):**
  - *Impacto:* Interrompe a contagem do Aceite Tácito. Retém o faturamento do marco até a disponibilização da correção.
  - *Rito de Reteste:* Disponibilizada a correção pela Contratada, abre-se a janela de **até 2 (dois) dias úteis**, adstrita exclusivamente à validação do defeito corrigido (sendo vedada reabertura de fluxos já aprovados).
- **Severidade P3 (Médio com contorno) ou P4 (Cosmético/Visual):**
  - *Impacto:* **NÃO retém o aceite do marco nem o faturamento**. O marco é considerado homologado e a correção é programada no ciclo de desenvolvimento subsequente.

---

## 4. Requisitos Obrigatórios de Evidência Técnica (5 Pontos de Reporte)
Para ter validade jurídica e técnica contratual, todo reporte de não conformidade formulado pelo PO do Cliente deve ser submetido com os 5 requisitos formais:
1. **URL / Rota / Endpoint exato:** `{{EVIDENCIA_URL}}`
2. **Payload / Parâmetros utilizados:** `{{EVIDENCIA_PAYLOAD}}`
3. **Passos determinísticos de reprodução:** Sequência numerada e reproduzível.
4. **Evidências técnicas auditáveis:** Prints com timestamp, gravação de tela, logs de console e captura de rede (HAR).
5. **Configuração do ambiente de teste:** Versão do navegador (últimas 3 versões de Chrome, Edge ou Safari), sistema operacional e resolução de tela.

*Reportes desprovidos destes requisitos são juridicamente ineficazes e não suspendem o relógio do Aceite Tácito.*

---

## 5. Salvaguarda de Instabilidade Externa de Legados
- Indisponibilidades, manutenções, timeouts ou falhas em APIs/sandboxes de responsabilidade do Cliente **NÃO suspendem nem interrompem** o prazo de homologação de 5 dias úteis.
- A conformidade do software da Contratada é formalmente comprovada por meio da execução de testes automatizados integrados com simuladores (mocks/stubs) no pipeline de CI/CD.

---

## 6. Checklist de Definition of Ready (DoR) do Card de QA
- [ ] Roteiro de testes estruturado com base nos cenários BDD das histórias de usuário vinculadas.
- [ ] Dados de teste sintéticos e anonimizados gerados em Staging (LGPD compliance).
- [ ] Mocks para serviços legados de terceiros configurados e validados.
- [ ] PO homologador do Cliente notificado formalmente sobre a data de início da janela de 5 dias úteis.

## 7. Checklist de Definition of Done (DoD) do Card de QA
- [ ] Execução de 100% dos testes planejados concluída com evidências arquivadas.
- [ ] Zero apontamentos abertos classificados como P1 ou P2.
- [ ] Eventuais defeitos corrigidos validados dentro da janela de reteste de até 2 dias úteis.
- [ ] Emissão do Termo de Aceite formal ou consumação jurídica do Aceite Tácito (5 dias úteis de silêncio do Cliente).
- [ ] Notificação de liberação de faturamento financeiro encaminhada ao setor financeiro/comercial.
