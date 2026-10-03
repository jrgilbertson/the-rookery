#!/usr/bin/env python3
"""Check the repository schema contract, not agent saving or source access."""

import copy
import json
import runpy
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
schema = runpy.run_path(str(HERE / "source-map-schema.py"))
validate = schema["validate"]
read_map = schema["read_map"]


class SourceMapSchemaChecks(unittest.TestCase):
    def setUp(self):
        self.v2 = read_map(HERE / "source-bindings/valid-v2.json")

    def test_shipped_sample(self):
        sample = read_map(HERE.parents[2] / "skills/personal-chief-of-staff/assets/sources.example.json")
        self.assertEqual(sample["version"], 3)
        roles = sample["roles"]
        self.assertTrue({"strategy", "learning", "tasks", "templates", "meetings"} <= roles.keys())
        self.assertEqual({entry["area"] for bindings in roles.values() for entry in bindings},
                         {"direction", "commitments", "relationships", "reflection",
                          "resources", "health", "leisure"})
        for role, area in (("reviews", "reflection"), ("templates", "reflection"),
                           ("meetings", "relationships")):
            self.assertTrue(all(entry["area"] == area for entry in roles[role]))
        self.assertTrue({entry["locator"] for entry in roles["reviews"]}.isdisjoint(
            entry["locator"] for entry in roles["templates"]))
        self.assertGreaterEqual(len(roles["relationships"]), 2)
        self.assertGreaterEqual(len(roles["conversations"]), 3)
        entries = [entry for bindings in sample["roles"].values() for entry in bindings]
        self.assertTrue(any(len(entry.get("access_overrides", {})) >= 2 for entry in entries))
        self.assertTrue(all("source" in entry for entry in entries))

    def test_versions_and_read_preserve_fixture_bytes(self):
        for name in ("valid.json", "valid-v2.json", "setup-initial.json"):
            path = HERE / "source-bindings" / name
            before = path.read_bytes()
            self.assertEqual(read_map(path), json.loads(before))
            self.assertEqual(path.read_bytes(), before)
        for version in (1, 2, 3):
            validate({"version": version, "roles": {}})

    def test_optional_and_custom_roles_need_no_migration(self):
        for version in (1, 2, 3):
            entry = {"area": "reflection", "interface": "document reader",
                     "identity": "fictional-notes", "locator": "templates-1",
                     "filter": "review templates; not evidence of completed activity"}
            if version < 3:
                entry.update(condition="bounded", modes=["weekly"])
            data = {"version": version, "roles": {"reviews": [entry],
                    "custom_context": [{**entry, "area": "custom_group"}]}}
            before = copy.deepcopy(data)
            with self.subTest(version=version):
                validate(data)
                self.assertEqual(data, before)

    def test_optional_source_without_overrides(self):
        entry = self.v2["roles"]["strategy"][0]
        del entry["access_overrides"]
        validate(self.v2)
        del entry["source"]
        validate(self.v2)

    def test_invalid_override_descriptions(self):
        valid = self.v2["roles"]["strategy"][0]["access_overrides"]["codex-desktop"]
        invalid = [{}, {"interface": "reader", "locator": "id"},
                   {**valid, "query": "id"},
                   {key: value for key, value in valid.items() if key != "locator"},
                   {**valid, "identity": " "},
                   {**valid, "window": "week"}, {**valid, "modes": ["weekly"]},
                   {**valid, "condition": "baseline"},
                   {**valid, "filter": "active"}, {**valid, "gap_effect": "limited"}]
        for override in invalid:
            with self.subTest(override=override):
                data = copy.deepcopy(self.v2)
                data["roles"]["strategy"][0]["access_overrides"] = {"codex-desktop": override}
                with self.assertRaises(ValueError):
                    validate(data)

    def test_invalid_binding_extensions(self):
        changes = [("source", " "), ("source", None), ("access_overrides", {}),
                   ("access_overrides", []), ("unknown", "value")]
        access = self.v2["roles"]["strategy"][0]["access_overrides"]["codex-desktop"]
        changes += [("access_overrides", {key: access}) for key in
                    ("Codex", "codex_desktop", "-codex", "codex--desktop", "codex-")]
        for key, value in changes:
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.v2)
                data["roles"]["strategy"][0][key] = value
                with self.assertRaises(ValueError):
                    validate(data)
        del self.v2["roles"]["strategy"][0]["source"]
        with self.assertRaises(ValueError):
            validate(self.v2)

    def test_v1_rejects_extensions_and_unknown_versions(self):
        for version in (1, 4, True, "2"):
            with self.subTest(version=version):
                data = copy.deepcopy(self.v2)
                data["version"] = version
                with self.assertRaises(ValueError):
                    validate(data)

    def test_legacy_field_constraints(self):
        for key, value in (("locator", " "), ("query", "second selector"),
                           ("condition", "conditional"), ("modes", ["weekly"]),
                           ("modes", ["weekly", "weekly"]), ("area", "")):
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.v2)
                data["roles"]["strategy"][0][key] = value
                with self.assertRaises(ValueError):
                    validate(data)
        with self.assertRaises(ValueError):
            validate({"version": 2, "roles": {"strategy": []}})

    def test_v3_rejects_workflow_fields_and_preserves_access_constraints(self):
        sample = read_map(HERE.parents[2] / "skills/personal-chief-of-staff/assets/sources.example.json")
        entry = sample["roles"]["strategy"][0]
        for key, value in (("condition", "baseline"), ("modes", ["weekly"])):
            with self.subTest(key=key), self.assertRaises(ValueError):
                changed = copy.deepcopy(sample)
                changed["roles"]["strategy"][0][key] = value
                validate(changed)
        del entry["access_overrides"]["codex-desktop"]["identity"]
        with self.assertRaises(ValueError):
            validate(sample)

    def test_invalid_json(self):
        for name in ("duplicate.json", "duplicate-nested.json", "malformed.txt", "unsupported.json"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                read_map(HERE / "source-bindings" / name)
        with self.assertRaises(ValueError):
            json.loads('{"version":2,"roles":{},"roles":{}}',
                       object_pairs_hook=schema["object_without_duplicates"])
        with self.assertRaises(ValueError):
            json.loads('{"version":NaN,"roles":{}}', parse_constant=schema["reject_constant"])


if __name__ == "__main__":
    unittest.main()
