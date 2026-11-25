"""Compare the original and stricter answer prompts on selected development cases."""
import json

from ask_nist import DATA, answer_with_local_model
from answer_ollama import STRICT_SYSTEM, generate
from evaluate_bm25 import BM25, ROOT, read_jsonl

CASES = ("nist-001", "nist-006", "nist-032", "nist-053", "nist-058")


def main():
    source = ROOT / "eval/review/development.jsonl"
    selected = {q["id"]: q for q in read_jsonl(source) if q["id"] in CASES}
    if set(selected) != set(CASES) or any(q["split"] != "development" for q in selected.values()):
        raise ValueError("Expected all five development cases.")
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    rows = read_jsonl(DATA / "chunks-A.jsonl")
    index = BM25(read_jsonl(DATA / "chunks-C.jsonl"))
    lines = [
        "# Focused prompt comparison", "",
        "Three controls with previously correct answers and two known false answers were "
        "selected from development. This targeted diagnostic is not an overall accuracy estimate. "
        "Both prompts ran live against the same local model and retrieved passages. "
        "The held-out set was not read.", "",
    ]

    def strict(question, passages):
        return generate(question, passages, system=STRICT_SYSTEM)

    def display(result):
        if result is None:
            return "Abstained."
        citations = ", ".join(f"AI {c['report_id']}, PDF p. {c['pdf_page']}"
                              for c in result["citations"])
        return f"{result['text']} ({citations})"

    for qid in CASES:
        item = selected[qid]
        original = answer_with_local_model(item["question"], labels, rows, index)
        revised = answer_with_local_model(item["question"], labels, rows, index, generate_answer=strict)
        lines.extend([f"## {qid}", "", item["question"], "",
                      f"**Expected** {item['expected_answer'] or 'Abstain.'}", "",
                      f"**Original** {display(original)}", "",
                      f"**Stricter** {display(revised)}", ""])
        print(f"{qid} original={display(original)}", flush=True)
        print(f"{qid} stricter={display(revised)}", flush=True)
    (ROOT / "eval/focused-prompt-comparison.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

