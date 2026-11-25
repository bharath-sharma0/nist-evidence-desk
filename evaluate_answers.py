"""Measure provisional answer and abstention behavior on development questions."""
import json
import re

from ask_nist import DATA, answer_question
from evaluate_bm25 import BM25, ROOT, normalize, read_jsonl


def comparable(text):
    return normalize(re.sub(r"\bregu-\s+larly\b", "regularly", text)).casefold()


def main():
    items = read_jsonl(ROOT / "eval/review/development.jsonl")
    if any(item["split"] != "development" for item in items):
        raise ValueError("Expected development questions only")
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    rows = read_jsonl(DATA / "chunks-A.jsonl")
    index = BM25(read_jsonl(DATA / "chunks-C.jsonl"))
    answered = hits = support = correct_abstentions = false_answers = 0
    answerable = sum(bool(item["evidence"]) for item in items)
    details = []
    for item in items:
        result = answer_question(item["question"], labels, rows, index)
        evidence = item["evidence"]
        if not evidence:
            correct_abstentions += result is None
            false_answers += result is not None
            status = "Abstained" if result is None else "Answered draft-unanswerable item"
        elif result is None:
            status = "Declined answerable item"
        else:
            answered += 1
            text = comparable(result["text"])
            page_matches = [
                e for e in evidence if
                result["url"].endswith(f"NIST.AI.{e['report_id']}.pdf#page={e['pdf_page']}")
            ]
            hits += bool(page_matches)
            # This measures quote coverage, not semantic answer correctness.
            covered = bool(page_matches) and all(
                e in page_matches and comparable(e["quote"]) in text for e in evidence
            )
            support += covered
            status = ("All labeled evidence quoted" if covered else
                      "Needs answer review" if page_matches else "Different page than gold")
        details.extend([f"## {item['id']} · {status}", "", item["question"], "",
                        f"Draft answer: {item['expected_answer'] or 'Abstain'}", "",
                        f"Program: {result['text']}" if result else "Program: abstained.", ""])
        if result:
            details.extend([f"Source: {result['citation']}", ""])
    unanswerable = len(items) - answerable
    summary = [
        "# Development answer diagnostic", "",
        "Runs the same extractive answer path as the command-line tool on provisional "
        "development labels. Quote coverage requires the returned text to contain every "
        "labeled excerpt with the matching page citation. It is a strict diagnostic, "
        "not a semantic correctness score. Human review is still needed.", "",
        f"- Answered {answered}/{answerable} answerable questions.",
        f"- Cited a labeled page on {hits}/{answerable} answerable questions.",
        f"- Quoted all labeled evidence on {support}/{answerable} answerable questions.",
        f"- Abstained on {correct_abstentions}/{unanswerable} draft-unanswerable questions "
        f"and answered the other {false_answers}.", "",
    ]
    (ROOT / "eval/development-answer-diagnostic.md").write_text(
        "\n".join(summary + details), encoding="utf-8")
    print("\n".join(summary[4:8]))


if __name__ == "__main__":
    main()

