"""Trace selected development failures without touching held-out data."""
from evaluate_bm25 import BM25, ROOT, covers, read_jsonl

CASES = ("nist-004", "nist-007", "nist-008", "nist-009")


def main():
    questions = read_jsonl(ROOT / "eval/review/development.jsonl")
    selected = {q["id"]: q for q in questions if q["id"] in CASES}
    if any(q["split"] != "development" for q in selected.values()):
        raise ValueError("Expected only development questions")
    lines = [
        "# Development retrieval failure audit", "",
        "BM25 was rerun at full depth for four recurring misses. A rank is the first "
        "positively scored chunk containing the full excerpt on the cited page. "
        "Unranked means a matching chunk exists but received no positive keyword score. "
        "Unavailable means no chunk contains the full excerpt.", "",
        "| Question and excerpt | Cited PDF page | A | B | C |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    indices = {}
    for strategy in "ABC":
        chunks = read_jsonl(ROOT / "data/processed" / f"chunks-{strategy}.jsonl")
        indices[strategy] = chunks, BM25(chunks)
    for key in CASES:
        item = selected[key]
        for number, evidence in enumerate(item["evidence"], 1):
            cells = []
            for strategy in "ABC":
                chunks, index = indices[strategy]
                if not any(covers(chunk, evidence) for chunk in chunks):
                    cells.append("Unavailable")
                    continue
                ranked = index.search(item["question"], k=len(chunks))
                rank = next((i for i, chunk in enumerate(ranked, 1)
                             if covers(chunk, evidence)), None)
                cells.append(str(rank) if rank else "Unranked")
            lines.append(f"| {key} excerpt {number} | AI {evidence['report_id']}, "
                         f"p. {evidence['pdf_page']} | " + " | ".join(cells) + " |")
    lines.extend(["", "## Query vocabulary check", "",
                  "The additional query below is a post-hoc diagnostic using the gold "
                  "term. It is not counted in the benchmark.", ""])
    question = selected["nist-004"]
    for strategy in "ABC":
        chunks, index = indices[strategy]
        for label, query in (("original", question["question"]),
                             ("with gold term", question["question"] + " confabulation")):
            rank = next((i for i, chunk in enumerate(index.search(query, len(chunks)), 1)
                         if covers(chunk, question["evidence"][0])), None)
            lines.append(f"- Strategy {strategy}, {label}: {rank if rank else 'unranked'}")
    output = ROOT / "eval/development-failure-audit.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[7:]))
    

if __name__ == "__main__":
    main()

