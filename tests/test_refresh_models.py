import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("refresh_models", ROOT / "scripts/refresh_models.py")
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "config/models.json").read_text())
        self.runtime = json.loads((ROOT / "config/runtime-models.json").read_text())

    def test_exact_runtime_ids_and_capabilities(self):
        result = refresh.runtime_config(self.config, self.runtime)
        self.assertEqual({m["id"] for m in result["models"]}, {m["id"] for m in self.runtime["models"]})
        self.assertIn("octodemo/Octodemo_Foundry/DeepSeek-V4-Flash", {m["id"] for m in result["models"]})
        for model in result["models"]:
            self.assertEqual(model, next(m for m in self.runtime["models"] if m["id"] == model["id"]))

    def test_bad_runtime_inputs(self):
        for mutation in ("duplicate", "auto", "capability", "empty", "markdown"):
            runtime = copy.deepcopy(self.runtime)
            if mutation == "duplicate":
                runtime["models"].append(runtime["models"][0])
            elif mutation == "auto":
                runtime["models"][0]["id"] = "auto"
            elif mutation == "capability":
                runtime["models"][0]["max_reasoning"] = "true"
            elif mutation == "markdown":
                runtime["models"][0]["name"] = "bad|name"
            else:
                runtime["models"] = []
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                refresh.runtime_config(self.config, runtime)

    def test_invalid_defaults_fail_closed(self):
        for mutation in ("unknown", "overlap", "provider"):
            config = copy.deepcopy(self.config)
            if mutation == "unknown":
                config["defaults"]["standard_judges"][0] = "guessed-model"
            elif mutation == "overlap":
                config["defaults"]["standard_judges"][0] = config["defaults"]["standard_contestants"][0]
            else:
                config["defaults"]["standard_judges"] = ["gpt-6-sol", "gpt-6.1-sol", "gpt-6.1-terra"]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                refresh.runtime_config(config, self.runtime)

    def test_docs_discovery_never_constructs_ids(self):
        markdown = "## Supported AI models in Copilot\n| Brand New Model | Vendor | GA |\n## Other\n"
        self.assertEqual(refresh.docs_models(markdown), ["Brand New Model"])
        for invalid in ("changed layout", "## Supported AI models in Copilot\n| no models |",
                        "## Supported AI models in Copilot\n| | Vendor | GA |"):
            with self.assertRaises(ValueError):
                refresh.docs_models(invalid)

    def test_marker_failure_does_not_mutate_any_target(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            good, bad = Path(directory) / "good.md", Path(directory) / "bad.md"
            original = refresh.BEGIN + "\nold\n" + refresh.END
            good.write_text(original)
            for content in ("missing", original + refresh.BEGIN, refresh.END + refresh.BEGIN):
                bad.write_text(content)
                with self.assertRaises(ValueError):
                    refresh.planned_updates(self.config, [good, bad])
                self.assertEqual(good.read_text(), original)

    def test_render_deduplicates_symlinks_and_check_is_read_only(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            target, alias = Path(directory) / "skill.md", Path(directory) / "alias.md"
            target.write_text(refresh.BEGIN + "\nold\n" + refresh.END)
            alias.symlink_to(target.name)
            with patch.object(refresh, "TARGETS", [target, alias]):
                with self.assertRaises(ValueError):
                    refresh.render(self.config, check=True)
                self.assertIn("old", target.read_text())
                updates = refresh.render(self.config)
                self.assertEqual(len(updates), 1)
                before = target.read_bytes()
                refresh.render(self.config, check=True)
                self.assertEqual(before, target.read_bytes())
                self.assertTrue(alias.is_symlink())

    def test_generated_rosters_match(self):
        refresh.render(self.config, check=True)


if __name__ == "__main__":
    unittest.main()
