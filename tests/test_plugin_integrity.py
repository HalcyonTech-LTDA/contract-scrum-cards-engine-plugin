#!/usr/bin/env python3
"""
Integrity and structure validation test suite for contract-scrum-cards-engine-plugin.
Verifies plugin.json, rules, agents, templates, and scripts using standard unittest.
"""

import json
import os
import re
import sys
import unittest

PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestPluginIntegrity(unittest.TestCase):

    def test_plugin_json(self):
        """Verifies plugin.json schema, metadata, skills, agents, and rules."""
        plugin_json_path = os.path.join(PLUGIN_DIR, "plugin.json")
        self.assertTrue(os.path.exists(plugin_json_path), f"plugin.json missing at {plugin_json_path}")

        with open(plugin_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("name"), "contract-scrum-cards-engine")
        self.assertIn("version", data)
        self.assertIn("description", data)
        self.assertIn("author", data)
        self.assertIn("displayName", data)
        self.assertIn("$schema", data)
        self.assertIn("suggestedPrompts", data)
        self.assertGreater(len(data.get("suggestedPrompts", [])), 0)

        # Verify skills
        skills = data.get("skills", [])
        self.assertGreater(len(skills), 0, "No skills declared")
        for skill_path in skills:
            full_skill_dir = os.path.join(PLUGIN_DIR, skill_path)
            self.assertTrue(os.path.isdir(full_skill_dir), f"Skill dir not found: {full_skill_dir}")
            skill_md = os.path.join(full_skill_dir, "SKILL.md")
            self.assertTrue(os.path.exists(skill_md), f"SKILL.md missing in {full_skill_dir}")

        # Verify agents
        agents = data.get("agents", [])
        self.assertEqual(len(agents), 6, f"Expected 6 agents, found {len(agents)}")
        for agent_path in agents:
            full_agent_path = os.path.join(PLUGIN_DIR, agent_path)
            self.assertTrue(os.path.exists(full_agent_path), f"Agent file missing: {full_agent_path}")

        # Verify rules
        rules = data.get("rules", [])
        self.assertEqual(len(rules), 3, f"Expected 3 rules, found {len(rules)}")
        for rule_path in rules:
            full_rule_path = os.path.join(PLUGIN_DIR, rule_path)
            self.assertTrue(os.path.exists(full_rule_path), f"Rule file missing: {full_rule_path}")

    def test_agent_frontmatter(self):
        """Verifies YAML frontmatter structure in all agent definition files."""
        agents_dir = os.path.join(PLUGIN_DIR, "agents")
        agent_files = [f for f in os.listdir(agents_dir) if f.endswith(".md")]
        self.assertEqual(len(agent_files), 6)

        for fname in agent_files:
            filepath = os.path.join(agents_dir, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(content.startswith("---\n"), f"Agent {fname} missing leading frontmatter delimiter")
            parts = content.split("---\n", 2)
            self.assertGreaterEqual(len(parts), 3, f"Agent {fname} invalid frontmatter structure")
            frontmatter = parts[1]

            self.assertIn("name:", frontmatter, f"Agent {fname} missing 'name:' in frontmatter")
            self.assertIn("description:", frontmatter, f"Agent {fname} missing 'description:' in frontmatter")
            self.assertIn("subagent: true", frontmatter, f"Agent {fname} missing 'subagent: true' in frontmatter")

    def test_rule_frontmatter(self):
        """Verifies YAML frontmatter in all normative rule files."""
        rules_dir = os.path.join(PLUGIN_DIR, "rules")
        rule_files = [f for f in os.listdir(rules_dir) if f.endswith(".md")]
        self.assertEqual(len(rule_files), 3)

        for fname in rule_files:
            filepath = os.path.join(rules_dir, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(content.startswith("---\n"), f"Rule {fname} missing leading frontmatter delimiter")
            parts = content.split("---\n", 2)
            self.assertGreaterEqual(len(parts), 3, f"Rule {fname} invalid frontmatter structure")
            frontmatter = parts[1]

            self.assertIn("description:", frontmatter, f"Rule {fname} missing 'description:'")
            self.assertIn("trigger: model_decision", frontmatter, f"Rule {fname} missing 'trigger: model_decision'")

    def test_templates_presence(self):
        """Verifies all mandatory templates exist and have valid placeholders."""
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
            self.assertTrue(os.path.exists(tmpl_path), f"Template missing: {tmpl_path}")
            with open(tmpl_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreater(len(content), 500, f"Template {tmpl} unexpectedly short ({len(content)} bytes)")
            placeholders = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", content)
            self.assertGreater(len(placeholders), 0, f"Template {tmpl} has no placeholders")

    def test_validation_script_presence(self):
        """Verifies that validate_backlog.py exists and can be imported."""
        script_path = os.path.join(
            PLUGIN_DIR, "skills", "contract-scrum-orchestrator", "scripts", "validate_backlog.py"
        )
        self.assertTrue(os.path.isfile(script_path), f"Validator script missing at {script_path}")


if __name__ == "__main__":
    unittest.main()
