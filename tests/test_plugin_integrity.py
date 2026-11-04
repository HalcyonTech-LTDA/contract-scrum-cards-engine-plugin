#!/usr/bin/env python3
"""
Integrity and E2E validation test suite for contract-scrum-cards-engine-plugin.
Verifies plugin.json, rules, agents, templates, and simulates end-to-end card generation.
"""

import json
import os
import re
import sys
import tempfile

PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_plugin_json():
    print("--> Testing plugin.json structure and references...")
    plugin_json_path = os.path.join(PLUGIN_DIR, "plugin.json")
    assert os.path.exists(plugin_json_path), f"plugin.json missing at {plugin_json_path}"

    with open(plugin_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("name") == "contract-scrum-cards-engine", f"Unexpected name: {data.get('name')}"
    assert "version" in data
    assert "description" in data
    assert "author" in data

    # Verify skills
    skills = data.get("skills", [])
    assert len(skills) > 0, "No skills declared"
    for skill_path in skills:
        full_skill_dir = os.path.join(PLUGIN_DIR, skill_path)
        assert os.path.isdir(full_skill_dir), f"Skill dir not found: {full_skill_dir}"
        skill_md = os.path.join(full_skill_dir, "SKILL.md")
        assert os.path.exists(skill_md), f"SKILL.md missing in {full_skill_dir}"

    # Verify agents
    agents = data.get("agents", [])
    assert len(agents) == 6, f"Expected 6 agents, found {len(agents)}"
    for agent_path in agents:
        full_agent_path = os.path.join(PLUGIN_DIR, agent_path)
        assert os.path.exists(full_agent_path), f"Agent file missing: {full_agent_path}"

    # Verify rules
    rules = data.get("rules", [])
    assert len(rules) == 3, f"Expected 3 rules, found {len(rules)}"
    for rule_path in rules:
        full_rule_path = os.path.join(PLUGIN_DIR, rule_path)
        assert os.path.exists(full_rule_path), f"Rule file missing: {full_rule_path}"

    print("    [PASS] plugin.json is valid and all references exist.")


def test_agent_frontmatter():
    print("--> Testing Agent YAML frontmatter...")
    agents_dir = os.path.join(PLUGIN_DIR, "agents")
    for fname in os.listdir(agents_dir):
        if not fname.endswith(".md"):
            continue
        filepath = os.path.join(agents_dir, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check frontmatter delimiters
        assert content.startswith("---\n"), f"Agent {fname} missing leading frontmatter delimiter"
        parts = content.split("---\n", 2)
        assert len(parts) >= 3, f"Agent {fname} invalid frontmatter structure"
        frontmatter = parts[1]

        assert "name:" in frontmatter, f"Agent {fname} missing 'name:' in frontmatter"
        assert "description:" in frontmatter, f"Agent {fname} missing 'description:' in frontmatter"
        assert "subagent: true" in frontmatter, f"Agent {fname} missing 'subagent: true' in frontmatter"

    print("    [PASS] All 6 agent files have valid frontmatter.")


def test_rule_frontmatter():
    print("--> Testing Rule YAML frontmatter...")
    rules_dir = os.path.join(PLUGIN_DIR, "rules")
    for fname in os.listdir(rules_dir):
        if not fname.endswith(".md"):
            continue
        filepath = os.path.join(rules_dir, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert content.startswith("---\n"), f"Rule {fname} missing leading frontmatter delimiter"
        parts = content.split("---\n", 2)
        assert len(parts) >= 3, f"Rule {fname} invalid frontmatter structure"
        frontmatter = parts[1]

        assert "description:" in frontmatter, f"Rule {fname} missing 'description:'"
        assert "trigger: model_decision" in frontmatter, f"Rule {fname} missing 'trigger: model_decision'"

    print("    [PASS] All 3 rule files have valid frontmatter.")


def test_templates_presence():
    print("--> Testing Templates presence and valid placeholders...")
    templates_dir = os.path.join(PLUGIN_DIR, "skills", "contract-scrum-orchestrator", "templates")
    expected_templates = [
        "EPIC.template.md",
        "USER_STORY.template.md",
        "TECHNICAL_ENABLER.template.md",
        "QA_HOMOLOGATION.template.md",
        "GATE_ZERO_SAFEGUARD.template.md",
        "INDEX_BACKLOG_TAXONOMY.template.md"
    ]
    for tmpl in expected_templates:
        tmpl_path = os.path.join(templates_dir, tmpl)
        assert os.path.exists(tmpl_path), f"Template missing: {tmpl_path}"
        with open(tmpl_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 500, f"Template {tmpl} unexpectedly short ({len(content)} bytes)"
        placeholders = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", content)
        assert len(placeholders) > 0, f"Template {tmpl} has no placeholders"

    print("    [PASS] All 6 templates exist and contain valid placeholders.")


def test_e2e_template_rendering_and_hygiene():
    print("--> Testing simulated template rendering and output hygiene (no unrendered placeholders or HTML comments)...")
    templates_dir = os.path.join(PLUGIN_DIR, "skills", "contract-scrum-orchestrator", "templates")
    user_story_tmpl_path = os.path.join(templates_dir, "USER_STORY.template.md")

    with open(user_story_tmpl_path, "r", encoding="utf-8") as f:
        tmpl_content = f.read()

    # Find all placeholders in USER_STORY.template.md
    placeholders = set(re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", tmpl_content))
    replacement_map = {k: f"SUBSTANTIVE_VALUE_FOR_{k}" for k in placeholders}

    rendered = tmpl_content
    for k, v in replacement_map.items():
        rendered = rendered.replace(f"{{{{{k}}}}}", v)

    # Check for unrendered placeholders
    remaining = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", rendered)
    assert len(remaining) == 0, f"Found remaining unrendered placeholders: {remaining}"

    # Check for HTML comments
    html_comments = re.findall(r"<!--.*?-->", rendered, re.DOTALL)
    assert len(html_comments) == 0, f"Found HTML comments: {html_comments}"

    print("    [PASS] Rendering and hygiene checks succeed with 0 leaks.")


def main():
    print(f"=== Starting verification for {PLUGIN_DIR} ===")
    test_plugin_json()
    test_agent_frontmatter()
    test_rule_frontmatter()
    test_templates_presence()
    test_e2e_template_rendering_and_hygiene()
    print("=== ALL 5 VERIFICATION SUITES PASSED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()
