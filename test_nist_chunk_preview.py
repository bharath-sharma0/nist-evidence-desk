import json
import unittest
from pathlib import Path

from extract_nist import validate_chunk_citations
from preview_nist_chunking import MAX_WORDS, STRATEGIES, load_pages, preview, word_count

ROOT = Path(__file__).parent / "data" / "processed"
PAGES = load_pages(ROOT)
LABELS = json.loads((ROOT / "nist-page-label-map.json").read_text(encoding="utf-8"))
TEXT = {(p["report_id"], p["pdf_page"]): p["text"] for p in PAGES}
CHUNKS = {strategy: list(preview(PAGES, strategy)) for strategy in STRATEGIES}


class ChunkPreviewTest(unittest.TestCase):
    def test_ids_are_deterministic_unique_and_independent_of_page_input_order(self):
        ids = []
        for strategy, chunks in CHUNKS.items():
            expected = [c["id"] for c in chunks]
            self.assertEqual(expected, [c["id"] for c in preview(list(reversed(PAGES)), strategy)])
            ids.extend(expected)
        self.assertEqual(len(ids), len(set(ids)))

    def test_written_datasets_match_the_validated_preview(self):
        for strategy, expected in CHUNKS.items():
            path = ROOT / f"chunks-{strategy}.jsonl"
            saved = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(saved, expected)

    def test_nonempty_and_bounded(self):
        for strategy, chunks in CHUNKS.items():
            self.assertTrue(chunks)
            for item in chunks:
                self.assertTrue(item["text"].strip(), item["id"])
                limit = MAX_WORDS if item["kind"] == "row" else (240 if strategy == "A" else 180)
                self.assertLessEqual(word_count(item["text"]), limit, item["id"])

    def test_all_text_can_be_found_on_cited_pages(self):
        for items in CHUNKS.values():
            validate_chunk_citations(items, LABELS, TEXT)

    def test_section_strategy_keeps_one_chunk_per_structured_row(self):
        rows = [item for item in CHUNKS["A"] if item["kind"] == "row"]
        self.assertEqual(len(rows), sum(len(p["rows"]) for p in PAGES))
        for page in PAGES:
            citations = [dict(report_id=page["report_id"], pdf_page=page["pdf_page"])]
            selected = [item["text"] for item in rows if item["citations"] == citations]
            expected = [" | ".join(row[key] for key in ("action_id", "suggested_action", "gai_risks"))
                        if "action_id" in row else " | ".join(value for value in row.values() if value)
                        for row in page["rows"]]
            self.assertEqual(selected, expected)

    def test_fixed_windows_overlap_by_30_words(self):
        page = next(p for p in PAGES if p["report_id"] == "100-1" and p["pdf_page"] == 34)
        first, second, *_ = preview([page], "B")
        self.assertEqual(first["text"].split()[-30:], second["text"].split()[:30])

    def test_sentence_strategy_keeps_numbered_heading_intact(self):
        page = next(p for p in PAGES if p["report_id"] == "600-1" and p["pdf_page"] == 51)
        self.assertTrue(any("A.1.2. Organizational Governance" in " ".join(c["text"].split())
                            for c in preview([page], "C")))

    def test_long_sentence_uses_size_fallback(self):
        p = dict(report_id="100-1", pdf_page=6, text=" ".join(["example"] * 181) + ".")
        self.assertEqual([word_count(c["text"]) for c in preview([p], "C")], [180, 1])


if __name__ == "__main__":
    unittest.main()




