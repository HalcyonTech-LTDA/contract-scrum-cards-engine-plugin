#!/usr/bin/env python3
"""
Automated Validator for Contract Scrum Backlogs.
Deterministically audits a generated contractual backlog directory for:
1. Physical directory partitioning (00_GATE_ZERO .. 05_GOVERNANCE_SAFEGUARDS + INDEX)
2. Zero HTML template comments (<!-- ... -->)
3. Zero unresolved placeholders ({{...}})
4. Strict Definition of Ready (DoR) and Definition of Done (DoD) on all cards
5. INVEST granularity sizing (teto de 8 Story Points por User Story)
6. Minimum 2 BDD/Gherkin scenarios per User Story (Happy Path & Exception)
7. NFR Latency (p95 < 500ms), 5-day Tacit Acceptance & 2-day Retest window
8. Bidirectional traceability between INDEX_BACKLOG_TAXONOMY.md and physical files.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

MANDATORY_DIRS = [
    "00_GATE_ZERO",
    "01_EPICS",
    "02_USER_STORIES",
    "03_TECHNICAL_ENABLERS",
    "04_QA_ACCEPTANCE",
    "05_GOVERNANCE_SAFEGUARDS",
]

INDEX_FILE_NAME = "INDEX_BACKLOG_TAXONOMY.md"


class BacklogValidationError(Exception):
    pass


def validate_backlog_structure(backlog_dir: str) -> List[str]:
    errors = []
    if not os.path.isdir(backlog_dir):
        return [f"Backlog root directory not found: {backlog_dir}"]

    index_path = os.path.join(backlog_dir, INDEX_FILE_NAME)
    if not os.path.isfile(index_path):
        errors.append(f"Master index file missing: {index_path}")

    for d in MANDATORY_DIRS:
        full_d = os.path.join(backlog_dir, d)
        if not os.path.isdir(full_d):
            errors.append(f"Mandatory subfolder missing: {d}")

    return errors


def audit_file_hygiene(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check 1: Minimum content
    if len(content.strip()) < 150:
        errors.append(f"{relpath}: Content too short ({len(content)} bytes)")

    # Check 2: Unresolved placeholders
    unresolved = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", content)
    if unresolved:
        errors.append(f"{relpath}: Found unresolved placeholders: {set(unresolved)}")

    # Check 3: HTML comments
    html_comments = re.findall(r"<!--.*?-->", content, re.DOTALL)
    if html_comments:
        errors.append(f"{relpath}: Found {len(html_comments)} residual HTML comment(s)")

    return errors


def audit_user_story(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # User persona check (allowing markdown bold/italics around keywords)
    has_persona = bool(
        re.search(r"\bComo\b[\*_\s]+.+", content, re.IGNORECASE)
        and re.search(r"\bQuero\b[\*_\s]+.+", content, re.IGNORECASE)
        and re.search(r"\bPara\s+que\b[\*_\s]+.+", content, re.IGNORECASE)
    )
    if not has_persona:
        errors.append(f"{relpath}: Missing canonical user persona framing ('Como ... Quero ... Para que ...')")

    # Story points check (INVEST <= 8 SP)
    sp_match = re.search(r"(\d+)\s*Story\s*Points?", content, re.IGNORECASE)
    if sp_match:
        sp = int(sp_match.group(1))
        if sp > 8:
            errors.append(f"{relpath}: Story exceeds INVEST limit of 8 SP ({sp} SP found)")
    else:
        errors.append(f"{relpath}: Missing Story Points estimate")

    # BDD Gherkin scenarios (at least 2: Dado / Quando / Então)
    scenarios = re.findall(r"Cen[áa]rio:\s*(.+)", content, re.IGNORECASE)
    if len(scenarios) < 2:
        errors.append(f"{relpath}: Requires at least 2 BDD Gherkin scenarios, found {len(scenarios)}")

    has_gherkin_steps = bool(
        re.search(r"Dado\s+que\s+.+", content, re.IGNORECASE)
        and re.search(r"Quando\s+.+", content, re.IGNORECASE)
        and re.search(r"Ent[ãa]o\s+.+", content, re.IGNORECASE)
    )
    if not has_gherkin_steps:
        errors.append(f"{relpath}: Incomplete BDD syntax (Dado / Quando / Então steps required)")

    # DoR and DoD checklists
    if not re.search(r"Definition\s+of\s+Ready|\bDoR\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Ready (DoR) section")
    if not re.search(r"Definition\s+of\s+Done|\bDoD\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Done (DoD) section")

    # Non-scope boundary
    if not re.search(r"N[ãa]o-Escopo|Out\s+of\s+Scope", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing explicit non-scope boundary section")

    return errors


def audit_epic(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"Marco\s+Contratual|Milestone", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing contractual milestone reference")
    if not re.search(r"Definition\s+of\s+Ready|\bDoR\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Ready (DoR) section")
    if not re.search(r"Definition\s+of\s+Done|\bDoD\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Done (DoD) section")

    return errors


def audit_enabler(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"Definition\s+of\s+Ready|\bDoR\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Ready (DoR) section")
    if not re.search(r"Definition\s+of\s+Done|\bDoD\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Done (DoD) section")
    if not re.search(r"Lat[êe]ncia|p95|500\s*ms", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing NFR latency / p95 specification")

    return errors


def audit_qa_homologation(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"Staging", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Staging test environment specification")
    if not re.search(r"5\s*(?:\(cinco\))?\s*dias\s+[úu]teis|Aceite\s+T[áa]cito|Deemed\s+Acceptance", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing 5-day Tacit Acceptance clause")
    if not re.search(r"2\s*(?:\(dois\))?\s*dias\s+[úu]teis|Janela\s+(?:Estrita\s+)?de\s+Reteste", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing 2-day Retest Window clause")
    if not re.search(r"P1|P2|P3|P4", content):
        errors.append(f"{relpath}: Missing P1-P4 defect severity rubric")
    if not re.search(r"Definition\s+of\s+Ready|\bDoR\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Ready (DoR) section")
    if not re.search(r"Definition\s+of\s+Done|\bDoD\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Done (DoD) section")

    return errors


def audit_safeguard(filepath: str, relpath: str) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"Definition\s+of\s+Ready|\bDoR\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Ready (DoR) section")
    if not re.search(r"Definition\s+of\s+Done|\bDoD\b", content, re.IGNORECASE):
        errors.append(f"{relpath}: Missing Definition of Done (DoD) section")

    return errors


def audit_traceability_matrix(backlog_dir: str) -> List[str]:
    errors = []
    index_path = os.path.join(backlog_dir, INDEX_FILE_NAME)
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Find all physical card files on disk
    physical_cards: Set[str] = set()
    for root, _, files in os.walk(backlog_dir):
        for fname in files:
            if fname.endswith(".md") and fname != INDEX_FILE_NAME:
                rel = os.path.relpath(os.path.join(root, fname), backlog_dir)
                if not rel.startswith("."):
                    physical_cards.add(rel)

    # Check that each physical card is referenced in index
    for card_rel in physical_cards:
        if card_rel not in index_content:
            errors.append(f"Orphan Card: Physical file '{card_rel}' is not referenced in {INDEX_FILE_NAME}")

    # Check for ghost cards (referenced in index but missing on disk)
    table_refs = re.findall(r"`((?:0[0-5]_[A-Z_]+)/[^`]+\.md)`", index_content)
    for ref in table_refs:
        full_ref_path = os.path.join(backlog_dir, ref)
        if not os.path.isfile(full_ref_path):
            errors.append(f"Ghost Card: Matrix references '{ref}' which does not exist on disk")

    return errors


def run_full_validation(backlog_dir: str) -> Tuple[bool, List[str]]:
    all_errors = []

    # 1. Structure
    struct_errors = validate_backlog_structure(backlog_dir)
    all_errors.extend(struct_errors)
    if struct_errors:
        return False, all_errors

    # 2. Iterate all md files
    for root, _, files in os.walk(backlog_dir):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, backlog_dir)
            if rel.startswith("."):
                continue

            # Hygiene
            all_errors.extend(audit_file_hygiene(fpath, rel))

            # Domain audits
            if "02_USER_STORIES" in rel:
                all_errors.extend(audit_user_story(fpath, rel))
            elif "01_EPICS" in rel:
                all_errors.extend(audit_epic(fpath, rel))
            elif "03_TECHNICAL_ENABLERS" in rel:
                all_errors.extend(audit_enabler(fpath, rel))
            elif "04_QA_ACCEPTANCE" in rel:
                all_errors.extend(audit_qa_homologation(fpath, rel))
            elif "00_GATE_ZERO" in rel or "05_GOVERNANCE_SAFEGUARDS" in rel:
                all_errors.extend(audit_safeguard(fpath, rel))

    # 3. Traceability
    all_errors.extend(audit_traceability_matrix(backlog_dir))

    return (len(all_errors) == 0), all_errors


def main():
    parser = argparse.ArgumentParser(description="Deterministic Contract Scrum Backlog Validator")
    parser.add_argument("backlog_dir", nargs="?", default="./backlog", help="Path to backlog root directory")
    args = parser.parse_args()

    backlog_dir = os.path.abspath(args.backlog_dir)
    print(f"=== Auditing Contract Scrum Backlog at: {backlog_dir} ===")

    success, errors = run_full_validation(backlog_dir)
    if success:
        print("[PASS] 100% of Backlog Cards, Structure, DoR/DoD and Traceability Matrix verified successfully.")
        sys.exit(0)
    else:
        print(f"[FAIL] Found {len(errors)} validation failure(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
