"""Test a separate claim-support check on five targeted development examples."""
import argparse
import json

from answer_ollama import verify_claims
from ask_nist import DATA, answer_with_local_model
from compare_qwen_prompts import CASES
from evaluate_bm25 import BM25, ROOT, read_jsonl


def main(include_table_context=False):
    selected = {q["id"]: q for q in read_jsonl(ROOT / "eval/review/development.jsonl")
                if q["id"] in CASES}
    if set(selected) != set(CASES) or any(q["split"] != "development" for q in selected.values()):
        raise ValueError("Expected the five targeted development examples.")
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    rows = read_jsonl(DATA / "chunks-A.jsonl")
    index = BM25(read_jsonl(DATA / "chunks-C.jsonl"))
    lines = [
        "# Claim-support check with table context" if include_table_context else "# Targeted claim-support check", "",
        "Qwen generated each draft separately. A second request to the same model saw "
        "the question, draft, and validated quotes, with source table context when enabled. This is a targeted development "
        "diagnostic. The check is experimental and the default CLI is unchanged.", "",
        "| Item | Expected | Draft | After evidence check |",
        "| --- | --- | --- | --- |",
    ]
    details = []
    for qid in CASES:
        item = selected[qid]
        draft = answer_with_local_model(item["question"], labels, rows, index)
        verdict = verify_claims(item["question"], draft, include_table_context=include_table_context) if draft else None
        kept = verdict is not None and verdict["supported"]
        expected = "Answer" if item["evidence"] else "Abstain"
        outcome = "Kept" if kept else "Abstained"
        lines.append(f"| {qid} | {expected} | {'Answer' if draft else 'Abstained'} | {outcome} |")
        details.extend(["", f"## {qid}", "", item["question"], "",
                        f"**Expected** {item['expected_answer'] or 'Abstain.'}", "",
                        f"**Draft** {draft['text'] if draft else 'Abstained.'}", "",
                        f"**Checker** {verdict['reason'] if verdict else 'No draft to verify.'}", ""])
        for quote in draft["quotes"] if draft else []:
            details.append(f"- {quote}")
        if include_table_context and draft:
            details.extend(f"- Full table row: {row}" for row in draft["table_context"])
        print(qid, expected, outcome, verdict, flush=True)
    name = "claim-support-with-table-context.md" if include_table_context else "claim-support-check.md"
    (ROOT / "eval" / name).write_text("\n".join(lines + details) + "\n",
                                                     encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table-context", action="store_true")
    main(parser.parse_args().table_context)


