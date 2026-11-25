import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from extract_nist import validate_chunk_citations
from nist_geometry import verify_footer

ROOT = Path(__file__).parent / "data" / "processed"
LABELS = json.loads((ROOT / "nist-page-label-map.json").read_text(encoding="utf-8"))
FOOTERS = json.loads((ROOT / "nist-footer-audit.json").read_text(encoding="utf-8"))
PAGES = {(p["report_id"], p["pdf_page"]): p for p in
         map(json.loads, (ROOT / "nist-pages.jsonl").read_text(encoding="utf-8").splitlines())}
TEXT = {key: page["text"] for key, page in PAGES.items()}


def cite(report, page):
    return {"report_id": report, "pdf_page": page}


def chunk(text, *citations):
    return {"id": "test", "text": text, "citations": citations}


class IngestionTest(unittest.TestCase):
    def test_map_matches_every_extracted_footer(self):
        self.assertEqual(set(LABELS), {"100-1", "600-1"})
        observed = {(entry["report_id"], entry["pdf_page"]): entry for entry in FOOTERS}
        self.assertEqual(set(observed), set(PAGES))
        self.assertEqual(len(FOOTERS), 112)
        for report, count in (("100-1", 48), ("600-1", 64)):
            self.assertEqual(set(LABELS[report]), {str(n) for n in range(1, count + 1)})
            for n in range(1, count + 1):
                entry = observed[report, n]
                actual = entry["extracted_footer"].removeprefix("Page").strip() or None
                self.assertEqual(LABELS[report][str(n)], actual)
        self.assertEqual([LABELS["100-1"][str(n)] for n in (1, 2, 3, 4, 5, 48)],
                         [None, None, None, "i", "ii", None])

    def test_incorrect_footer_fails(self):
        band = SimpleNamespace(extract_text=lambda **_: "Page 30")
        page = SimpleNamespace(crop=lambda _: band, width=612, height=792, page_number=34)
        with self.assertRaisesRegex(ValueError, "expected footer"):
            verify_footer(page, "100-1", "29")

    def test_citation_requires_real_text_on_cited_page(self):
        phrase = "Confabulations can occur across GAI outputs and contexts"
        validate_chunk_citations([chunk(phrase, cite("600-1", 10))], LABELS, TEXT)
        for invalid in (chunk(phrase, cite("600-1", 11)),
                        chunk("Invented wording", cite("600-1", 10)),
                        chunk("", cite("600-1", 10))):
            with self.assertRaisesRegex(ValueError, "Chunk text absent"):
                validate_chunk_citations([invalid], LABELS, TEXT)

    def test_invalid_and_missing_citations(self):
        for invalid in (cite("100-1", 49), cite("unknown", 1), cite("600-1", "51")):
            with self.assertRaisesRegex(ValueError, "Unknown cited page"):
                validate_chunk_citations([chunk("text", cite("600-1", 10), invalid)], LABELS, TEXT)
        with self.assertRaisesRegex(ValueError, "Missing citations"):
            validate_chunk_citations([chunk("text")], LABELS, TEXT)

    def test_measure_table_cells_and_continuation(self):
        first = PAGES["100-1", 34]
        continuation = PAGES["100-1", 35]
        self.assertEqual(len(first["rows"]), 2)
        self.assertIn("Appropriate methods", first["rows"][0]["category"])
        self.assertNotIn("MEASURE 1.1", first["rows"][0]["category"])
        self.assertIn("selected for implementation", first["rows"][0]["subcategories"])
        self.assertNotIn("MEASURE 1.1", first["layout_text"])
        self.assertIn("MEASURE 2.6", continuation["rows"][0]["subcategories"])

    def test_multi_row_actions_and_cross_page_text(self):
        first = PAGES["600-1", 18]
        next_page = PAGES["600-1", 19]
        rows = [row for page in (first, next_page) for row in page["rows"]
                if row["action_id"].startswith("GV-1.3-")]
        self.assertEqual([r["action_id"] for r in rows], [f"GV-1.3-{i:03}" for i in range(1, 8)])
        for row in rows:
            self.assertEqual(set(row), {"action_id", "suggested_action", "gai_risks", "actor_tasks"})
            self.assertEqual(row["actor_tasks"], "Governance and Oversight")
            self.assertTrue(all(row.values()))
        self.assertNotIn("GV-1.3-003", first["layout_text"])
        self.assertNotIn("GV-1.3-004", next_page["layout_text"])
        cross_page = first["text"].splitlines()[-1] + "\n" + next_page["text"].splitlines()[0]
        validate_chunk_citations([chunk(cross_page, cite("600-1", 18), cite("600-1", 19))],
                                 LABELS, TEXT)
        with self.assertRaisesRegex(ValueError, "Chunk text absent"):
            validate_chunk_citations([chunk(cross_page, cite("600-1", 19), cite("600-1", 18))],
                                     LABELS, TEXT)

    def test_two_column_reading_order(self):
        self.assertLess(TEXT["600-1", 51].index("Alignment to organizational values"),
                        TEXT["600-1", 51].index("Auditing and assessment"))
        self.assertLess(TEXT["600-1", 52].index("Opt-outs"),
                        TEXT["600-1", 52].index("Risk-based controls"))
        self.assertIn("interdisciplinary teams", TEXT["600-1", 52])


if __name__ == "__main__":
    unittest.main()


