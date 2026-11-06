import importlib.util
import copy
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hackathon_rules", ROOT / "scripts/hackathon_rules.py")
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)


class RulesTests(unittest.TestCase):
    def test_legacy_ratings_and_corrupt_counts_or_receipts(self):
        legacy = {"models": {"retired-model": {"elo": 1500.5, "wins": 4, "losses": 2, "total": 3}},
                  "updated": "2026-11-05T12:00:00Z"}
        self.assertEqual(rules.validate_elo_data(legacy), legacy)
        mutations = [
            ("elo", float("nan")), ("elo", True), ("wins", -1),
            ("losses", 1.5), ("total", True), ("recent_results", ["imagined"]),
        ]
        for field, value in mutations:
            data = copy.deepcopy(legacy)
            data["models"]["retired-model"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                rules.validate_elo_data(data)
        for receipts in (["run-1", "run-1"], [""], "run-1"):
            with self.assertRaises(ValueError):
                rules.validate_elo_data({**legacy, "applied_run_ids": receipts})
        with self.assertRaises(ValueError):
            rules.validate_elo_data({**legacy, "updated": "not-a-date"})

    def test_brackets_cover_all_models_without_singleton_heats(self):
        for count in range(101):
            with self.subTest(count=count):
                sizes = rules.bracket_sizes(count)
                self.assertEqual(sum(sizes), count)
                if count > 4:
                    self.assertEqual(len(sizes), math.ceil(count / 4))
                    self.assertTrue(all(2 <= size <= 4 for size in sizes))
                    self.assertLessEqual(max(sizes) - min(sizes), 1)
        self.assertEqual(rules.bracket_sizes(12), [4, 4, 4])
        for invalid in (-1, 2.5, True):
            with self.assertRaises(ValueError):
                rules.bracket_sizes(invalid)

    def test_explicit_mode_and_no_accidental_mass_launch(self):
        self.assertEqual(rules.select_mode("full review of this skill; go deep"), "classic")
        self.assertEqual(rules.select_mode("haiku", explicit="metaswarm"), "metaswarm")
        self.assertEqual(rules.select_mode("architecture", explicit="classic"), "classic")
        self.assertEqual(rules.select_mode("build a full REST API"), "tournament")
        with self.assertRaises(ValueError):
            rules.select_mode("haiku", explicit="unknown")

    def test_votes_do_not_call_tied_pairs_a_majority(self):
        for votes, expected in (
            (["A", "A", "A", "B"], "CONSENSUS"),
            (["A", "A", "B", "C"], "PAIR AGREEMENT"),
            (["A", "A", "B", "B"], "CONFLICT"),
            (["A", "A", "A", "B", "B", "B"], "CONFLICT"),
            (["A", "B", "C"], "UNIQUE"),
        ):
            with self.subTest(votes=votes):
                self.assertEqual(rules.classify_votes(votes), expected)
        with self.assertRaises(ValueError):
            rules.classify_votes([])

    def test_elo_is_order_independent_zero_sum_and_handles_ties(self):
        ratings = {"A": 1600, "B": 1500, "C": 1400}
        scores = {"A": 40, "B": 40, "C": 30}
        updated = rules.elo_updates(ratings, scores)
        reordered = rules.elo_updates(dict(reversed(list(ratings.items()))), scores)
        self.assertEqual(updated, reordered)
        self.assertAlmostEqual(sum(updated.values()), sum(ratings.values()))
        self.assertEqual(rules.elo_updates({"A": 1500, "B": 1500}, {"A": 40, "B": 40}),
                         {"A": 1500, "B": 1500})
        self.assertEqual(ratings["A"], 1600)
        for invalid in (float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                rules.elo_updates({"A": 1500}, {"A": invalid})

    def test_sideline_pending_and_failed_work_are_not_invented_successes(self):
        records = [
            {"contestant": "A", "status": "completed", "evidence": "receipt-A"},
            {"contestant": "B", "status": "running", "evidence": "launch-B"},
            {"contestant": "C", "status": "failed", "evidence": "failure-C"},
        ]
        report = rules.sideline_report(records, "build -> judging")
        self.assertEqual((report["finished"], report["successful"], report["remaining"]), (2, 1, 1))
        self.assertEqual(report["decision"], "pending")
        self.assertTrue(all(row["score"] == "pending" for row in report["contestants"]))
        self.assertEqual(report["contestants"][1]["strengths"], "pending")

    def test_sideline_requires_score_and_status_evidence(self):
        valid = {"contestant": "A", "status": "completed", "evidence": "receipt",
                 "score": 42, "score_evidence": "judge-packet", "strengths": "edge cases covered"}
        report = rules.sideline_report([valid], "judging -> synthesis", "A advances")
        self.assertEqual(report["contestants"][0]["score"], 42)
        self.assertEqual(report["decision"], "A advances")
        for change in ({"evidence": ""}, {"score_evidence": ""}, {"score": float("nan")},
                       {"score": 51}, {"status": "running"}, {"status": "imagined"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                rules.sideline_report([{**valid, **change}], "judging")
        with self.assertRaises(ValueError):
            rules.sideline_report([valid, valid], "judging")


if __name__ == "__main__":
    unittest.main()
