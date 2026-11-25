"""Evaluate local Qwen on development data without accessing held-out items."""
import hashlib
import json
from time import perf_counter

from ask_nist import DATA, answer_with_local_model
from answer_ollama import MODEL
from evaluate_bm25 import BM25, ROOT, read_jsonl

EVAL = ROOT / "eval"


def key(citation):
    return citation["report_id"], citation["pdf_page"]


def main():
    source = EVAL / "review/development.jsonl"
    questions = read_jsonl(source)
    if any(item["split"] != "development" for item in questions):
        raise ValueError("Expected only development questions.")
    a = DATA / "chunks-A.jsonl"
    c = DATA / "chunks-C.jsonl"
    inputs = (source, a, c, ROOT / "answer_ollama.py", ROOT / "ask_nist.py")
    fingerprint = hashlib.sha256()
    for path in inputs:
        fingerprint.update(path.read_bytes())
    checkpoint = DATA / f"qwen-development-{fingerprint.hexdigest()[:16]}.jsonl"
    completed = {record["id"]: record for record in read_jsonl(checkpoint)} if checkpoint.exists() else {}
    rows = read_jsonl(a)
    index = BM25(read_jsonl(c))
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    for seq, item in enumerate(questions, 1):
        if item["id"] in completed:
            continue
        start = perf_counter()
        result = answer_with_local_model(item["question"], labels, rows, index)
        record = dict(id=item["id"], result=result, seconds=round(perf_counter() - start, 2))
        with checkpoint.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        completed[item["id"]] = record
        if seq % 5 == 0:
            print(f"Completed {seq}/{len(questions)}", flush=True)

    answerable = abstention = answered = matching = all_pages = correct_abstentions = 0
    details = []
    for item in questions:
        record = completed[item["id"]]
        result = record["result"]
        gold = {key(e) for e in item["evidence"]}
        cited = {key(e) for e in result["citations"]} if result else set()
        if gold:
            answerable += 1
            answered += result is not None
            matching += bool(gold & cited)
            all_pages += gold <= cited
            status = ("Declined answerable item" if not result else
                      "All labeled pages cited" if gold <= cited else
                      "Some labeled pages cited" if gold & cited else "No labeled page cited")
        else:
            abstention += 1
            correct_abstentions += result is None
            status = "Abstained" if result is None else "Answered draft-unanswerable item"
        details.extend([f"## {item['id']} · {status}", "", item["question"], "",
                        f"Draft answer: {item['expected_answer'] or 'Abstain'}", "",
                        f"Qwen: {result['text'] if result else 'Abstained.'}", ""])
        if cited:
            details.extend(["Pages: " + ", ".join(
                f"AI {report}, PDF page {page}" for report, page in sorted(cited)
            ), ""])
    summary = [
        "# Local Qwen development diagnostic", "",
        f"Model: {MODEL}. Uses the same retrieval, prompt, and citation checking as the CLI. "
        "Development labels are provisional. Page matches measure citation overlap; "
        "they do not establish answer correctness or full textual support.", "",
        f"- Answered {answered}/{answerable} answerable items.",
        f"- Cited at least one labeled page on {matching}/{answerable} answerable items.",
        f"- Cited every labeled page on {all_pages}/{answerable} answerable items.",
        f"- Abstained on {correct_abstentions}/{abstention} draft-unanswerable items.", "",
    ]
    (EVAL / "development-qwen-diagnostic.md").write_text(
        "\n".join(summary + details), encoding="utf-8")
    print("\n".join(summary[4:8]), flush=True)


if __name__ == "__main__":
    main()

