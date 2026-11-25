"""Summarize recorded judgments for the frozen browser-app evaluation."""
from collections import Counter
from statistics import median

from evaluate_bm25 import ROOT, read_jsonl

EVAL = ROOT / "eval"


def main():
    gold = {r["id"]: r for r in read_jsonl(EVAL / "review/heldout-frozen.jsonl")}
    outputs = read_jsonl(EVAL / "heldout-app-outputs.jsonl")
    notes = {r["id"]: r for r in read_jsonl(EVAL / "heldout-app-judgments.jsonl")}
    assert len(outputs) == len(gold) == len(notes) == 20
    assert set(gold) == set(notes) == {r["id"] for r in outputs}
    answerable = [r for r in outputs if gold[r["id"]]["evidence"]]
    unanswerable = [r for r in outputs if not gold[r["id"]]["evidence"]]
    answered = [r for r in answerable if r["answer"] is not None]
    correct = [r for r in answered if notes[r["id"]]["correct"]]
    supported_correct = sum(notes[r["id"]]["citation_support"] for r in correct)
    proper_abstentions = sum(r["answer"] is None for r in unanswerable)
    modes = Counter(r["mode"] or "abstained" for r in outputs)
    lines = [
        "# Held-out browser app evaluation", "",
        "One recorded response per item from the frozen 20-question draft, using local "
        "Qwen with the browser app's extractive fallback. Labels and responses were "
        "reviewed by the assistant. An answer is correct only if it covers all essential "
        "facts without contradiction. Evidence support requires the displayed passages "
        "to substantiate those facts. The set is small and some items share source rows.", "",
        "| Metric | Result |", "| --- | ---: |",
        f"| Returned an answer on answerable questions | {len(answered)}/{len(answerable)} |",
        f"| Correct answers | {len(correct)}/{len(answerable)} |",
        f"| Correct answers with supporting displayed passages | {supported_correct}/{len(answerable)} |",
        f"| Correct abstentions | {proper_abstentions}/{len(unanswerable)} |",
        f"| Correct overall, including abstentions | {len(correct) + proper_abstentions}/{len(outputs)} |",
        f"| Median local request time | {median(r['seconds'] for r in outputs):.1f} s |", "",
        f"Response modes across all items: {modes['qwen']} generated, "
        f"{modes['extractive']} source excerpts, {modes['abstained']} abstentions.", "",
    ]
    for result in outputs:
        item = gold[result["id"]]
        judgment = notes[result["id"]]
        outcome = ("Correct abstention" if result["answer"] is None and not item["evidence"] else
                   "Abstained on answerable question" if result["answer"] is None else
                   "Correct and supported" if judgment["correct"] and judgment["citation_support"] else
                   "Correct, incomplete support" if judgment["correct"] else "Incorrect or incomplete")
        lines.extend([f"## {result['id']} · {outcome}", "",
                      item["question"], "", f"**Expected** {item['expected_answer'] or 'Abstain.'}", "",
                      f"**App** {result['answer'] or 'Abstained.'}", "",
                      f"**Review** {judgment['note']}", ""])
        for source in result["sources"]:
            lines.extend([f"- {source['citation']} — {source['text']}", ""])
    (EVAL / "heldout-app-results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[6:14]))


if __name__ == "__main__":
    main()

