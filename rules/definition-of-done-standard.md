---
description: Padrão normativo de Definition of Done (DoD) aplicável obrigatoriamente para conclusão e homologação de cards ágeis derivados de anexos técnicos contratuais.
trigger: model_decision
---

# DEFINITION OF DONE (DoD) PARA CARDS DERIVADOS DE CONTRATOS

O **Definition of Done (DoD)** define o conjunto taxativo e inegociável de critérios técnicos, de segurança e de conformidade contratual que devem ser integralmente atendidos para que um card seja considerado concluído (`DONE`) pela Squad e disponibilizado para homologação contratual em Staging perante o Product Owner do Cliente, nos termos do **Anexo 3 (Protocolo de Homologação)**.

---

## 1. Qualidade de Código e Análise Estática
- Código-fonte escrito em estrita observância aos padrões arquiteturais do projeto.
- Análise estática de código (linters e scanners de segurança) executada na esteira de CI com **zero vulnerabilidades críticas ou altas** e conformidade total com as regras de estilo.
- Ausência de débitos técnicos não documentados ou métodos depreciados sem justificativa.

## 2. Cobertura de Testes Automatizados
- **Testes Unitários:** Implementados para todas as regras de negócio centrais, atingindo cobertura mínima de **80% de linhas e ramificações (branches)**.
- **Testes de Integração / API:** Suítes automatizadas cobrindo todos os cenários BDD/Gherkin especificados no card, validados contra contratos OpenAPI/Swagger.
- Todos os testes executados com sucesso em ambiente de CI/CD sem dependência de passos manuais.

## 3. Conformidade com Requisitos Não-Funcionais (NFRs)
- **Latência e Throughput:** Rotas de API e consultas a banco de dados testadas e aprovadas com tempo de resposta p95 inferior a **500ms**, atendendo à premissa do Anexo 1.
- **Resiliência a Falhas:** Tratamento adequado de erros com códigos HTTP semânticos (4xx/5xx), logs estruturados e mensagens de erro sem vazamento de stacktrace ou dados sensíveis.

## 4. Conformidade Estrita com a LGPD em Ambientes de Engenharia (Anexo 2)
- Ambientes de Desenvolvimento e Staging populados **exclusivamente com dados sintéticos, mockados ou anonimizados**.
- **Vedação Pétrea:** Comprovação de inexistência de dumps de produção contendo dados pessoais reais (PII) desprovidos de anonimização irreversível prévia, em conformidade com o papel da Contratada como Operadora técnica e do Cliente como Controlador.

## 5. Deploy Automatizado em Ambiente de Staging
- Artefato compilado, versionado e implantado com sucesso no ambiente oficial de **Staging** via pipeline de entrega contínua (CI/CD).
- Endpoints de verificação de integridade (*healthchecks*) e rotas principais retornando status `200 OK` de forma estável.

## 6. Documentação Técnica e Atualização de Contratos de API
- Especificação OpenAPI / Swagger devidamente atualizada com novos schemas, endpoints, headers de autenticação e códigos de resposta.
- Registro de Release Note sintético associado ao card, contendo escopo entregue, impactos de configuração e migrações de banco aplicadas.

## 7. Revisão por Pares (Pull Request / Code Review)
- Pull Request auditado e formalmente aprovado por no mínimo um Tech Lead ou Engenheiro Sênior da Contratada.
- Verificação de ausência de segredos, credenciais ou tokens embutidos no código-fonte (*hardcoded secrets*).

## 8. Prontidão para Homologação e Disparo do Aceite Tácito (Anexo 3)
- Pacote de evidências técnicas de funcionamento gerado e anexado ao card (prints, gravações de fluxo e payloads de teste validados).
- Notificação formal de entrega enviada ao Product Owner do Cliente, marcando o início da **contagem regressiva de 5 (cinco) dias úteis para homologação em Staging**.
- **Regra de Defeitos e Reteste:** Garantia de que eventuais reportes P1/P2 formulados pelo PO do Cliente observarão a janela de reteste de até 2 (dois) dias úteis adstrita ao defeito, sem reabertura de escopo.
- **Resiliência a Legados:** Caso sistemas legados do cliente apresentem indisponibilidade externa, a conclusão é comprovada via relatório de testes automatizados com mocks/stubs no CI/CD.
