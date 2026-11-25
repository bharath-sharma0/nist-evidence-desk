"""Check evaluation drafts against the pinned corpus and split policy."""
import unittest

from evaluate_bm25 import ROOT, normalize, read_jsonl

REVIEW = ROOT / "eval/review"


def page_keys(items):
    return {(e["report_id"], e["pdf_page"]) for item in items
            for e in item["evidence"] + item.get("related_pages", [])}


class EvaluationDraftTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dev = read_jsonl(REVIEW / "development.jsonl")
        cls.heldout = read_jsonl(REVIEW / "heldout.jsonl")
        cls.pages = {(p["report_id"], p["pdf_page"]): p for p in
                     read_jsonl(ROOT / "data/processed/nist-pages.jsonl")}

    def test_split_is_unique_and_keeps_the_pilot_in_development(self):
        self.assertEqual((len(self.dev), len(self.heldout)), (40, 20))
        all_items = self.dev + self.heldout
        self.assertEqual(len({q["id"] for q in all_items}), 60)
        self.assertEqual(len({q["question"] for q in all_items}), 60)
        self.assertTrue(all(q["split"] == "development" for q in self.dev))
        self.assertTrue(all(q["split"] == "heldout" for q in self.heldout))
        pilot = {q["id"] for q in read_jsonl(ROOT / "eval/questions.jsonl")}
        self.assertEqual({q["id"] for q in self.dev if q["origin"] == "pilot"}, pilot)
        self.assertTrue(all(q["origin"] == "expansion" for q in self.heldout))
        self.assertFalse(page_keys(self.dev) & page_keys(self.heldout))

    def test_evidence_and_abstention_schema(self):
        for q in self.dev + self.heldout:
            with self.subTest(item=q["id"]):
                if q["type"] == "unanswerable":
                    self.assertIsNone(q["expected_answer"])
                    self.assertEqual(q["evidence"], [])
                else:
                    self.assertTrue(q["expected_answer"])
                    self.assertTrue(q["evidence"])
                for e in q["evidence"]:
                    p = self.pages[e["report_id"], e["pdf_page"]]
                    self.assertEqual(e["printed_page"], p["printed_page"])
                    self.assertTrue(e["quote"])
                    self.assertIn(normalize(e["quote"]), normalize(p["text"]))
                    if "action_id" in e:
                        row = next(r for r in p["rows"] if r["action_id"] == e["action_id"])
                        self.assertIn(normalize(e["quote"]), normalize(row[e["field"]]))

