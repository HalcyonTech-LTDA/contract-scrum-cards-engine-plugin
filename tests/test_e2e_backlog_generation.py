#!/usr/bin/env python3
"""
End-to-End Simulation and Edge Case Test Suite for contract-scrum-cards-engine-plugin.
Uses standard unittest.TestCase and validate_backlog to verify full generation, DoR/DoD,
INVEST limits, BDD syntax, output hygiene, and bidirectional traceability.
"""

import os
import re
import shutil
import sys
import tempfile
import unittest

PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(PLUGIN_DIR, "skills", "contract-scrum-orchestrator", "templates")
SCRIPTS_DIR = os.path.join(PLUGIN_DIR, "skills", "contract-scrum-orchestrator", "scripts")

sys.path.insert(0, SCRIPTS_DIR)
import validate_backlog  # noqa: E402


def load_template(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(content: str, mapping: dict) -> str:
    result = content
    for k, v in mapping.items():
        result = result.replace(f"{{{{{k}}}}}", str(v))
    # Strip any residual HTML comments if present
    result = re.sub(r"<!--.*?-->", "", result, flags=re.DOTALL)
    return result


class TestE2EBacklogGeneration(unittest.TestCase):

    def setUp(self):
        self.output_dir = tempfile.mkdtemp(prefix="contract_backlog_test_")
        for d in validate_backlog.MANDATORY_DIRS:
            os.makedirs(os.path.join(self.output_dir, d), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, ".scratch"), exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def _generate_valid_backlog(self):
        """Helper that populates self.output_dir with a 100% valid, compliant backlog."""
        # 1. Gate Zero
        gz_tmpl = load_template("GATE_ZERO_SAFEGUARD.template.md")
        gz_rendered = render_template(
            gz_tmpl,
            {
                "CARD_ID": "GZ-001",
                "SAFEGUARD_TITLE": "Liberação Integral de Acessos e Ambientes",
                "SAFEGUARD_CATEGORY": "Gate Zero / Marco Zero",
                "GOVERNANCE_CLAUSE_REF": "[ANEXO_2_RACI-SEC-3-GATE-ZERO]",
                "GOVERNANCE_LEAD_ASSIGNEE": "Tech Lead HalcyonTech",
                "CLIENT_FOCAL_POINT": "PO Banco Alpha",
                "STATUS_CARD": "PENDING_CLEARANCE",
                "SAFEGUARD_DESCRIPTION_AND_MECHANISM": (
                    "Condição precedente de eficácia do cronograma de desenvolvimento. "
                    "A contagem dos dias do projeto somente se inicia após assinatura bilateral "
                    "do Termo de Liberação Integral de Acessos e Ambientes."
                ),
                "CONDITIONAL_TRIGGER_MILESTONE": "Início da Sprint 1 / M0",
                "RESPONSE_SLA_LIMIT": "Até 2 dias úteis de expediente comercial (16 horas úteis)",
                "DEFAULT_CONSEQUENCE": "Schedule Freeze dia-a-dia sem ônus para a Contratada",
                "LGPD_SAFEGUARD_CLAUSE": (
                    "Cliente como Controlador, Contratada como Operadora. Vedação total de dumps de produção com PII."
                ),
                "VERIFICATION_ITEM_1": "Credenciais em nuvem com privilégios mínimos configuradas",
                "VERIFICATION_ITEM_2": "Acesso a repositórios Git corporativos liberado",
                "VERIFICATION_ITEM_3": "VPN e túneis de conexão Staging validados",
                "VERIFICATION_ITEM_4": "Termo de Liberação assinado pelo PO do Cliente",
                "DOCUMENT_PROOF_TYPE": "Termo de Liberação Integral de Acessos assinado",
            },
        )
        with open(os.path.join(self.output_dir, "00_GATE_ZERO", "GZ-001-LIBERACAO-ACESSOS-AMBIENTES.md"), "w", encoding="utf-8") as f:
            f.write(gz_rendered)

        # 2. Epic
        epic_tmpl = load_template("EPIC.template.md")
        epic_rendered = render_template(
            epic_tmpl,
            {
                "CARD_ID": "EPIC-01",
                "EPIC_TITLE": "Fundação e Motor de Conciliação Bancária",
                "CONTRATO_MARCO_REF": "Marco M1 - Conciliação Core",
                "SOW_CLAUSE_REF": "[ANEXO_1_SOW-SEC-4-MARCO-01]",
                "MODELO_CONTRATACAO": "Modo A (Fixed Price por Milestones)",
                "PERCENTUAL_FATURAMENTO": "30% do Valor Global do Contrato",
                "RACI_RESPONSAVEL_CONTRATADA": "Squad Lead HalcyonTech",
                "RACI_APROVADOR_PO_CLIENTE": "Product Owner Titular Banco Alpha",
                "STATUS_CARD": "READY",
                "DESCRICAO_EXECUTIVA_ESCOPO": (
                    "Entrega do motor central de conciliação com suporte a arquivos OFX e conciliação em lote."
                ),
                "ENTREGAVEL_FISICO_1": "Serviço de parsing e validação de extratos bancários OFX",
                "ENTREGAVEL_FISICO_2": "Interface Web de conciliação com filtros por data e status",
                "ENTREGAVEL_FISICO_3": "Relatório sintético de divergências em Staging",
                "NAO_ESCOPO_ITEM_1": "Saneamento de dados bancários legados anteriores a 2024",
                "NAO_ESCOPO_ITEM_2": "Aplicativos móveis nativos iOS/Android",
                "CHILD_CARD_ID_1": "US-0101",
                "CHILD_CARD_TYPE_1": "User Story",
                "CHILD_CARD_TITLE_1": "Upload e Validação de Arquivo OFX",
                "CHILD_CARD_SP_1": "5",
                "CHILD_CARD_RESP_1": "Backend Dev",
                "CHILD_CARD_STATUS_1": "READY",
                "CHILD_CARD_ID_2": "ENABLER-0101",
                "CHILD_CARD_TYPE_2": "Enabler",
                "CHILD_CARD_TITLE_2": "Pipeline de Ingestão e Latência < 500ms",
                "CHILD_CARD_SP_2": "3",
                "CHILD_CARD_RESP_2": "Tech Lead",
                "CHILD_CARD_STATUS_2": "READY",
            },
        )
        with open(os.path.join(self.output_dir, "01_EPICS", "EPIC-01-FUNDACAO-CONCILIACAO.md"), "w", encoding="utf-8") as f:
            f.write(epic_rendered)

        # 3. User Story
        us_tmpl = load_template("USER_STORY.template.md")
        us_rendered = render_template(
            us_tmpl,
            {
                "CARD_ID": "US-0101",
                "STORY_TITLE": "Upload e Processamento de Extrato Bancário OFX",
                "PARENT_EPIC_REF": "EPIC-01 - Fundação e Motor de Conciliação",
                "SOW_CLAUSE_REF": "[ANEXO_1_SOW-SEC-3.1-ITEM-01]",
                "STORY_POINTS": "5",
                "PRIORITY": "Alta",
                "TECH_ASSIGNEE": "Backend Dev Senior",
                "CLIENT_PO": "PO Titular Banco Alpha",
                "STATUS_CARD": "READY",
                "USER_PERSONA": "Analista Financeiro do Banco",
                "ACTION_AND_CAPABILITY": (
                    "enviar um arquivo de extrato em formato OFX via interface web"
                ),
                "MEASURABLE_BUSINESS_BENEFIT": (
                    "reconciliar automaticamente as transações com a base interna sem retrabalho manual"
                ),
                "BUSINESS_RULE_1": "Arquivos superiores a 50MB devem ser rejeitados com código HTTP 413.",
                "BUSINESS_RULE_2": "Transações com hash idêntico em menos de 24h são marcadas como duplicadas.",
                "BUSINESS_RULE_3": "Todos os registros gravados recebem auditoria com ID do usuário e timestamp UTC.",
                "OUT_OF_SCOPE_ITEM_1": "Importação de extratos em formato PDF não estruturado.",
                "OUT_OF_SCOPE_ITEM_2": "Disparo automático de pagamentos a fornecedores.",
                "GHERKIN_SCENARIO_1_TITLE": "Upload com sucesso de arquivo OFX válido",
                "GHERKIN_SCENARIO_1_GIVEN": "o analista financeiro está autenticado e na tela de conciliação",
                "GHERKIN_SCENARIO_1_WHEN": "ele submete um arquivo OFX válido de 10MB",
                "GHERKIN_SCENARIO_1_THEN": (
                    "o sistema deve processar as transações em menos de 500ms e exibir resumo com status 200 OK"
                ),
                "GHERKIN_SCENARIO_2_TITLE": "Rejeição de arquivo malformado",
                "GHERKIN_SCENARIO_2_GIVEN": "o analista submete um arquivo com cabeçalho inválido",
                "GHERKIN_SCENARIO_2_WHEN": "o motor de validação executa o parse",
                "GHERKIN_SCENARIO_2_THEN": (
                    "o sistema deve retornar erro 422 com mensagem detalhando a linha inconsistente"
                ),
                "OPENAPI_SPEC_REFERENCE": "POST /api/v1/reconciliation/ofx-upload",
                "DATABASE_ENTITIES": "tb_statement_uploads, tb_bank_transactions",
            },
        )
        with open(os.path.join(self.output_dir, "02_USER_STORIES", "US-0101-UPLOAD-OFX.md"), "w", encoding="utf-8") as f:
            f.write(us_rendered)

        # 4. Enabler
        enabler_tmpl = load_template("TECHNICAL_ENABLER.template.md")
        enabler_rendered = render_template(
            enabler_tmpl,
            {
                "CARD_ID": "ENABLER-0101",
                "ENABLER_TITLE": "Motor de Mock e Resiliência a Sandboxes Legadas",
                "TECHNICAL_CATEGORY": "Mock-Resiliência e Arquitetura",
                "SYSTEM_COMPONENT": "Gateway de Integração Bancária",
                "NFR_OR_SOW_CLAUSE_REF": "[ANEXO_1_SOW-SEC-5-PREMISSA-01]",
                "STORY_POINTS": "3",
                "TECH_LEAD_ASSIGNEE": "Tech Lead HalcyonTech",
                "STATUS_CARD": "READY",
                "TECHNICAL_CONTEXT_AND_OBJECTIVE": (
                    "Garantir a não interrupção da homologação em Staging perante o PO "
                    "mesmo quando o ERP legado do Cliente sofrer instabilidade ou indisponibilidade, "
                    "em conformidade estrita com o Anexo 3."
                ),
                "TECHNICAL_DELIVERABLE_1": "WireMock server provisionado com schemas de transações",
                "TECHNICAL_DELIVERABLE_2": "Contrato OpenAPI com schemas de retorno e erro",
                "TECHNICAL_DELIVERABLE_3": "Suite de testes em CI/CD validando fallback para mock",
                "MAX_P95_LATENCY": "350",
                "TARGET_CONCURRENCY": "200",
                "ACCEPTANCE_CRITERION_1": "Latência p95 < 500ms atestada sob 200 conexões simultâneas.",
                "ACCEPTANCE_CRITERION_2": "Fallback automático para mock em caso de timeout legado > 2s.",
                "ACCEPTANCE_CRITERION_3": "Logs estruturados sem vazamento de tokens ou dados sensíveis.",
            },
        )
        with open(os.path.join(self.output_dir, "03_TECHNICAL_ENABLERS", "ENABLER-0101-MOCK-LEGADO.md"), "w", encoding="utf-8") as f:
            f.write(enabler_rendered)

        # 5. QA Homologation
        qa_tmpl = load_template("QA_HOMOLOGATION.template.md")
        qa_rendered = render_template(
            qa_tmpl,
            {
                "CARD_ID": "QA-0101",
                "QA_TITLE": "Roteiro de Homologação em Staging - Marco M1",
                "TARGET_EPIC_REF": "EPIC-01 - Fundação e Motor de Conciliação",
                "HOMOLOGATION_CLAUSE_REF": "[ANEXO_3_PROTOCOLO_HOMOLOGACAO-SEC-1]",
                "QA_LEAD_ASSIGNEE": "QA Lead HalcyonTech",
                "CLIENT_PO_EVALUATOR": "PO Titular Banco Alpha",
                "STATUS_CARD": "STAGING_DEPLOYED",
                "HOMOLOGATION_SCOPE_DESCRIPTION": (
                    "Validação dos fluxos de conciliação bancária OFX em Staging perante o PO do Cliente, "
                    "com disparo da contagem regressiva de 5 dias úteis para Aceite Tácito."
                ),
                "TEST_CASE_ID_1": "TC-01",
                "TEST_CASE_STORY_1": "US-0101",
                "TEST_CASE_TYPE_1": "E2E Automatizado",
                "TEST_CASE_PRECOND_1": "Ambiente Staging com massa sintética LGPD",
                "TEST_CASE_EXPECTED_1": "Upload de OFX concluído e conciliado com HTTP 200",
                "TEST_CASE_STATUS_1": "PASSED",
                "TEST_CASE_ID_2": "TC-02",
                "TEST_CASE_STORY_2": "US-0101",
                "TEST_CASE_TYPE_2": "Manual com Evidência",
                "TEST_CASE_PRECOND_2": "Arquivo OFX corrompido submetido",
                "TEST_CASE_EXPECTED_2": "Mensagem amigável de erro e status 422",
                "TEST_CASE_STATUS_2": "PASSED",
                "EVIDENCIA_URL": "https://staging.bancoalpha.internal/api/v1/reconciliation/ofx-upload",
                "EVIDENCIA_PAYLOAD": "multipart/form-data; file=extrato_teste_sintetico.ofx",
            },
        )
        with open(os.path.join(self.output_dir, "04_QA_ACCEPTANCE", "QA-0101-HOMOLOGACAO-M1.md"), "w", encoding="utf-8") as f:
            f.write(qa_rendered)

        # 6. Governance Safeguard
        gov_tmpl = load_template("GATE_ZERO_SAFEGUARD.template.md")
        gov_rendered = render_template(
            gov_tmpl,
            {
                "CARD_ID": "GOV-001",
                "SAFEGUARD_TITLE": "Conformidade LGPD e Gestão de Massa Sintética em Staging",
                "SAFEGUARD_CATEGORY": "LGPD Privacy",
                "GOVERNANCE_CLAUSE_REF": "[ANEXO_2_RACI-SEC-6-LGPD]",
                "GOVERNANCE_LEAD_ASSIGNEE": "SecOps Lead HalcyonTech",
                "CLIENT_FOCAL_POINT": "DPO / PO Banco Alpha",
                "STATUS_CARD": "ACTIVE_MONITORING",
                "SAFEGUARD_DESCRIPTION_AND_MECHANISM": (
                    "Cliente atua como Controlador e a Contratada como Operadora técnica. "
                    "Vedação contratual absoluta ao envio de dados reais de produção com PII sem anonimização prévia."
                ),
                "CONDITIONAL_TRIGGER_MILESTONE": "Durante todo o ciclo de desenvolvimento e homologação",
                "RESPONSE_SLA_LIMIT": "Imediato",
                "DEFAULT_CONSEQUENCE": (
                    "Incidente reportado formalmente e expurgo imediato de base não anonimizada"
                ),
                "LGPD_SAFEGUARD_CLAUSE": "Conformidade com Anexo 2, Seção 6",
                "VERIFICATION_ITEM_1": "Script de geração de dados sintéticos Faker homologado",
                "VERIFICATION_ITEM_2": "Auditoria de banco Staging sem CPF/dados reais de clientes",
                "VERIFICATION_ITEM_3": "Logs de aplicação configurados com mascaramento de dados",
                "VERIFICATION_ITEM_4": "Termo de não-transferência de dados de produção assinado",
                "DOCUMENT_PROOF_TYPE": "Relatório de Auditoria de Dados Sintéticos Staging",
            },
        )
        with open(os.path.join(self.output_dir, "05_GOVERNANCE_SAFEGUARDS", "GOV-001-CONFORMIDADE-LGPD.md"), "w", encoding="utf-8") as f:
            f.write(gov_rendered)

        # 7. Master Index
        idx_tmpl = load_template("INDEX_BACKLOG_TAXONOMY.template.md")
        rows = [
            "| [ANEXO_2_RACI-SEC-3] | GZ-001 | Gate Zero | Liberação Integral de Acessos | `00_GATE_ZERO/GZ-001-LIBERACAO-ACESSOS-AMBIENTES.md` | ATENDIDO | ATENDIDO |",
            "| [ANEXO_1_SOW-SEC-4] | EPIC-01 | Épico | Fundação e Motor de Conciliação | `01_EPICS/EPIC-01-FUNDACAO-CONCILIACAO.md` | ATENDIDO | ATENDIDO |",
            "| [ANEXO_1_SOW-SEC-3.1] | US-0101 | História | Upload de Extrato OFX | `02_USER_STORIES/US-0101-UPLOAD-OFX.md` | ATENDIDO | ATENDIDO |",
            "| [ANEXO_1_SOW-SEC-5] | ENABLER-0101 | Enabler | Motor de Mock e Resiliência | `03_TECHNICAL_ENABLERS/ENABLER-0101-MOCK-LEGADO.md` | ATENDIDO | ATENDIDO |",
            "| [ANEXO_3_HOMOLOG-SEC-1] | QA-0101 | QA | Roteiro de Homologação M1 | `04_QA_ACCEPTANCE/QA-0101-HOMOLOGACAO-M1.md` | ATENDIDO | ATENDIDO |",
            "| [ANEXO_2_RACI-SEC-6] | GOV-001 | Salvaguarda | Conformidade LGPD Dados Sintéticos | `05_GOVERNANCE_SAFEGUARDS/GOV-001-CONFORMIDADE-LGPD.md` | ATENDIDO | ATENDIDO |",
        ]
        idx_rendered = render_template(
            idx_tmpl,
            {
                "PROJETO_NOME": "Portal de Conciliação Financeira",
                "CLIENTE_NOME": "Banco Alpha S.A.",
                "CONTRATADA_NOME": "HalcyonTech Engenharia",
                "MODELO_CONTRATACAO": "Modo A (Fixed Price por Milestones)",
                "CONTRATO_MESTRE_REF": "ANEXO_TECNICO_MESTRE_CONTRATO.md",
                "DATA_GERACAO": "2026-11-04",
                "GATE_ZERO_OVERALL_STATUS": "CLEARED",
                "TOTAL_EPICS_COUNT": "1",
                "TOTAL_STORIES_COUNT": "1",
                "TOTAL_ENABLERS_COUNT": "1",
                "TOTAL_QA_COUNT": "1",
                "TOTAL_SAFEGUARDS_COUNT": "2",
                "TOTAL_STORY_POINTS": "8",
                "TABELA_RASTREABILIDADE_LINHAS": "\n".join(rows),
            },
        )
        with open(os.path.join(self.output_dir, "INDEX_BACKLOG_TAXONOMY.md"), "w", encoding="utf-8") as f:
            f.write(idx_rendered)

    def test_e2e_valid_generation_passes_all_checks(self):
        """Verifies that a fully generated backlog passes 100% of validation checks."""
        self._generate_valid_backlog()
        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertTrue(success, f"Expected validation to succeed, but got errors: {errors}")
        self.assertEqual(len(errors), 0)

    def test_invest_story_points_ceiling_detection(self):
        """Verifies that a User Story exceeding 8 Story Points is detected and rejected."""
        self._generate_valid_backlog()
        us_file = os.path.join(self.output_dir, "02_USER_STORIES", "US-0101-UPLOAD-OFX.md")
        with open(us_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Alter SP to 13 (violating INVEST limit of 8)
        content = content.replace("5 Story Points", "13 Story Points")
        with open(us_file, "w", encoding="utf-8") as f:
            f.write(content)

        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertFalse(success)
        self.assertTrue(any("INVEST limit of 8 SP" in e for e in errors), f"Expected INVEST error, got {errors}")

    def test_unresolved_placeholder_detection(self):
        """Verifies that any unrendered placeholder {{...}} triggers validation failure."""
        self._generate_valid_backlog()
        us_file = os.path.join(self.output_dir, "02_USER_STORIES", "US-0101-UPLOAD-OFX.md")
        with open(us_file, "a", encoding="utf-8") as f:
            f.write("\n\nTexto adicional com {{PLACEHOLDER_LEAK}} não resolvido.\n")

        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertFalse(success)
        self.assertTrue(any("unresolved placeholders" in e for e in errors), f"Expected placeholder error, got {errors}")

    def test_residual_html_comment_detection(self):
        """Verifies that any leftover HTML comment <!-- ... --> triggers failure."""
        self._generate_valid_backlog()
        epic_file = os.path.join(self.output_dir, "01_EPICS", "EPIC-01-FUNDACAO-CONCILIACAO.md")
        with open(epic_file, "a", encoding="utf-8") as f:
            f.write("\n<!-- Comentário de template esquecido -->\n")

        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertFalse(success)
        self.assertTrue(any("residual HTML comment" in e for e in errors), f"Expected HTML comment error, got {errors}")

    def test_orphan_card_detection(self):
        """Verifies that an extra physical card not listed in the Index is flagged as an Orphan Card."""
        self._generate_valid_backlog()
        orphan_path = os.path.join(self.output_dir, "02_USER_STORIES", "US-9999-EXTRA-UNTRACKED.md")
        with open(os.path.join(self.output_dir, "02_USER_STORIES", "US-0101-UPLOAD-OFX.md"), "r", encoding="utf-8") as f:
            content = f.read()
        with open(orphan_path, "w", encoding="utf-8") as f:
            f.write(content)

        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertFalse(success)
        self.assertTrue(any("Orphan Card" in e for e in errors), f"Expected Orphan Card error, got {errors}")

    def test_ghost_card_detection(self):
        """Verifies that a matrix row referencing a nonexistent card is flagged as Ghost Card."""
        self._generate_valid_backlog()
        idx_file = os.path.join(self.output_dir, "INDEX_BACKLOG_TAXONOMY.md")
        with open(idx_file, "a", encoding="utf-8") as f:
            f.write("\n| [ANEXO_1_SOW-SEC-9] | US-8888 | História | Fantasma | `02_USER_STORIES/US-8888-GHOST.md` | ATENDIDO | ATENDIDO |\n")

        success, errors = validate_backlog.run_full_validation(self.output_dir)
        self.assertFalse(success)
        self.assertTrue(any("Ghost Card" in e for e in errors), f"Expected Ghost Card error, got {errors}")


if __name__ == "__main__":
    unittest.main()
