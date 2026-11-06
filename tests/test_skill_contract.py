import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skill", ROOT / "tests/validate_skill.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillContractTests(unittest.TestCase):
    def setUp(self):
        self.content = (ROOT / "skills/havoc-hackathon/SKILL.md").read_text()

    def test_sideline_contract_rejects_missing_handoffs_or_evidence(self):
        result = validator.ValidationResult()
        validator.check_sideline_reporting(self.content, "skill", result)
        self.assertTrue(result.success, result.failed)
        for missing in ("Tournament every heat", "user status request",
                        "applied/unchanged/failed integration", "Scores"):
            result = validator.ValidationResult()
            validator.check_sideline_reporting(self.content.replace(missing, ""), "mutant", result)
            self.assertFalse(result.success, f"Missing {missing} must fail validation")

    def test_roster_validation_rejects_custom_id_drift(self):
        result = validator.ValidationResult()
        content = self.content.replace("octodemo/Octodemo_Foundry/DeepSeek-V4-Flash", "guessed-id")
        validator.check_model_roster(content, "mutant", result)
        self.assertFalse(result.success)

    def test_dry_run_does_not_authorize_automatic_live_probes(self):
        section = self.content.split("### Model Availability (explicit live check only)", 1)[1].split("### Output Format", 1)[0]
        self.assertIn("Offline preflight stops without model calls", section)
        self.assertIn("Only an explicit user request", section)
        self.assertNotIn("After simulation passes, dispatch", self.content)
        telemetry = self.content.split("## Telemetry (explicit opt-in)", 1)[1]
        self.assertIn("Default is off", telemetry)
        self.assertNotIn("curl", telemetry)


if __name__ == "__main__":
    unittest.main()
