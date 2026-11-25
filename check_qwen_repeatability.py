"""Repeat verdict-only claim checks on fixed development drafts."""
from concurrent.futures import ThreadPoolExecutor
import re

from answer_ollama import verify_verdict
from compare_qwen_prompts import CASES
from evaluate_bm25 import ROOT, read_jsonl

REPEATS = 3


def fixed_drafts():
    """Reuse the exact generated draft, quotes, and rows from the prior check."""
    report = (ROOT / "eval/claim-support-with-table-context.md").read_text(encoding="utf-8")
    drafts = {}
    sections = re.split(r"(?m)^## (nist-\d+)$", report)
    for key, section in zip(sections[1::2], sections[2::2]):
        draft = re.search(r"(?m)^\*\*Draft\*\* (.+)$", section)
        if draft is None or draft[1] == "Abstained.":
            raise ValueError(f"No fixed draft for {key}")
        quotes = []
        rows = []
        for line in section.splitlines():
            if line.startswith("- Full table row: "):
                rows.append(line.removeprefix("- Full table row: "))
            elif line.startswith("- "):
                quotes.append(line[2:])
        if not quotes:
            raise ValueError(f"No evidence quotes for {key}")
        drafts[key] = {"text": draft[1], "quotes": quotes, "table_context": rows}
    return drafts


def main():
    items = {q["id"]: q for q in read_jsonl(ROOT / "eval/review/development.jsonl")
             if q["split"] == "development"}
    drafts = fixed_drafts()
    report = [
        "# Repeated verdict-only evidence checks", "",
        "The same five generated answers and validated evidence from the prior check were "
        "reused. The model was asked for one boolean per request. The three answerable controls "
        "were manually checked as supported. The two false answers were manually checked as "
        "unsupported. This is a targeted development diagnostic.", "",
        "| Case | Expected | Run 1 | Run 2 | Run 3 | Consistent |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    consistent = correct = 0
    for key in CASES:
        try:
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(verify_verdict, items[key]["question"], drafts[key])
                           for _ in range(REPEATS)]
                results = [future.result() for future in futures]
        except ValueError as exc:
            raise RuntimeError(f"{key} returned a malformed verdict") from exc
        expected = bool(items[key]["evidence"])
        agreement = len(set(results)) == 1
        consistent += agreement
        correct += sum(value == expected for value in results)
        words = ["Supported" if value else "Unsupported" for value in [expected, *results]]
        report.append(f"| {key} | " + " | ".join(words) + f" | {'Yes' if agreement else 'No'} |")
        print(key, words, f"consistent={agreement}", flush=True)
    report.extend(["", f"{consistent}/{len(CASES)} cases gave the same verdict on all three runs.",
                   f"{correct}/{len(CASES) * REPEATS} individual verdicts matched the manual expectation.", ""])
    (ROOT / "eval/verdict-repeatability.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{consistent}/{len(CASES)} consistent; {correct}/{len(CASES) * REPEATS} correct.")


if __name__ == "__main__":
    main()

