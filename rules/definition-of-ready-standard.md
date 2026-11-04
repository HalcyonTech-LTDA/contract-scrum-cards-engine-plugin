---
description: Padrão normativo de Definition of Ready (DoR) aplicável obrigatoriamente a cards ágeis derivados de anexos técnicos contratuais (SOW, RACI, Homologação, CR e SLA).
trigger: model_decision
---

# DEFINITION OF READY (DoR) PARA CARDS DERIVADOS DE CONTRATOS

O **Definition of Ready (DoR)** constitui a barreira formal de qualidade técnica e jurídica que impede a entrada de itens ambíguos, incompletos ou desalinhados do contrato no ciclo ativo de desenvolvimento (Sprints/Milestones). Nenhum card pode ser categorizado como `READY` ou puxado para execução sem satisfazer integralmente os 8 pilares normativos abaixo:

---

## 1. Ancoragem e Rastreabilidade Contratual Estrita
- Todo card deve conter obrigatoriamente no cabeçalho a tag de rastreabilidade formal referenciando a seção ou anexo do contrato de origem:
  - Exemplos: `[SOW-SEC-3.1-MOD-01]`, `[RACI-EVENTO-02]`, `[HOMOLOG-CL-03]`, `[SLA-GARANTIA-CL-05]`.
- É terminantemente vedada a criação de cards sem vínculo contratual explícito. Demandas externas ou novas ideias que não constem nos anexos devem ser canalizadas para o protocolo de Change Request (Anexo 4).

## 2. Estruturação Substantiva e Personas Definidas
- A narrativa deve seguir o formato canônico:
  - `Como [ator/persona de negócio claramente tipificada]`
  - `Quero [capacidade delimitada descrita por substantivos técnicos auditáveis]`
  - `Para que [benefício de negócio mensurável e verificável]`
- **Regra Anti-Ambiguidade:** É proibido o uso de verbos vagos ("fazer telas", "otimizar fluxo", "trabalhar na API"). O escopo deve detalhar a ação concreta sobre dados, entidades e interfaces (ex.: "Interface Web para reconciliação bancária diária com upload de arquivo OFX e validação de duplicidade").

## 3. Critérios de Aceite em Formato BDD / Gherkin (Mínimo de 2 Cenários)
- Todo card deve conter no mínimo 2 cenários estruturados em sintaxe Gherkin formal:
  - Pelo menos 1 cenário de **Caminho Feliz (Happy Path)**;
  - Pelo menos 1 cenário de **Exceção, Erro ou Validação de Fronteira (Edge Case)**.
- Sintaxe obrigatória:
  ```gherkin
  Cenário: [Identificação clara do caso de teste]
    Dado que [estado inicial do sistema e pré-condições autenticadas]
    Quando [ação concreta disparada pelo usuário ou serviço externo]
    Então [resultado mensurável, código HTTP, estado do banco de dados e feedback visual]
  ```
- Critérios subjetivos ("layout agradável", "boa performance", "fácil de usar") são nulos e invalidam o DoR.

## 4. Pré-Requisitos Técnicos e Premissas Condicionantes Identificados
- Devem estar explicitados no card:
  - Contratos de API (especificação OpenAPI/Swagger documentada);
  - Schemas de dados e migrações de banco necessários;
  - Sandboxes externas necessárias e premissa de latência (tempo de resposta p95 < 500ms nas rotas integradas);
  - Dependências de credenciais, certificados mTLS ou chaves de API.

## 5. Delimitação Explícita de Não-Escopo (Boundaries)
- O card deve listar expressamente o que NÃO faz parte de sua entrega, em consonância com as exclusões contratuais do Anexo 1:
  - Sem suporte a navegadores legados (Chrome, Safari e Edge últimas 3 versões apenas);
  - Sem higienização de bases legadas;
  - Sem desenvolvimento de app móvel nativo quando o escopo for Web responsivo;
  - Sem absorção de custos transacionais de gateways/mensageria.

## 6. Governança RACI e Interlocutor Único
- O card deve indicar o papel responsável pela validação:
  - Product Owner do Cliente formalmente designado no Anexo 2 como homologador exclusivo;
  - Engenheiro responsável da Contratada (Squad Dev/Tech Lead).
- Indicação clara se a entrega depende de insumo do Cliente com disparo do SLA de resposta (até 2 dias úteis de expediente comercial / 16 horas úteis).

## 7. Dimensionamento de Esforço e Granularidade (INVEST)
- O card deve estar estimado pela equipe técnica em Story Points (sequência de Fibonacci: 1, 2, 3, 5, 8).
- **Teto de Granularidade:** Cards com estimativa superior a 8 Story Points violam o princípio INVEST (Small) e devem ser obrigatoriamente fatiados em histórias menores antes de atingir o status `READY`.

## 8. Verificação de Dependência do Gate Zero
- O card deve verificar se os pré-requisitos estruturais do Marco Zero (Gate Zero do Anexo 2) foram formalmente assinados no "Termo de Liberação Integral de Acessos e Ambientes".
- Nenhum card de desenvolvimento funcional de Milestone pode transicionar para execução sem que o Marco Zero esteja formalmente deferido.
