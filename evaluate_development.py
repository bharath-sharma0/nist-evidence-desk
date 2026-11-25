"""Run a provisional BM25 diagnostic on the development draft only."""
from collections import Counter

from evaluate_bm25 import ROOT, evaluate, read_jsonl


def main():
    questions = read_jsonl(ROOT / "eval/review/development.jsonl")
    if any(q["split"] != "development" for q in questions):
        raise ValueError("Expected only development questions")
    answerable = [q for q in questions if q["evidence"]]
    types = {q["id"]: q["type"] for q in answerable}
    counts = Counter(types.values())
    report = [
        "# Provisional BM25 development diagnostic", "",
        f"Scored {len(answerable)} answerable development items. "
        f"The {len(questions) - len(answerable)} abstention items are excluded. "
        "Draft gold labels still require manual review.", "",
        "| Chunking | Evidence Recall@5 | Complete | Fully retrievable in corpus |",
        "| --- | ---: | ---: | ---: |",
    ]
    details = []
    for strategy in "ABC":
        chunks = read_jsonl(ROOT / "data/processed" / f"chunks-{strategy}.jsonl")
        results = evaluate(chunks, answerable)
        fractions = [sum(rank is not None for rank in row["ranks"]) / len(row["ranks"])
                     for row in results]
        complete = sum(value == 1 for value in fractions)
        available = sum(row["available"] == len(row["ranks"]) for row in results)
        total = len(results)
        report.append(f"| {strategy} | {sum(fractions) / total:.1%} | "
                      f"{complete}/{total} | {available}/{total} |")
        details.extend(["", f"## Strategy {strategy}", "",
                        "| Question type | Evidence Recall@5 | Complete |",
                        "| --- | ---: | ---: |"])
        for kind, count in sorted(counts.items()):
            group = [value for row, value in zip(results, fractions) if types[row["id"]] == kind]
            details.append(f"| {kind} | {sum(group) / count:.1%} | {sum(v == 1 for v in group)}/{count} |")
        details.extend(["", "| Question | Type | Evidence ranks | Excerpts present anywhere |",
                        "| --- | --- | --- | ---: |"])
        for row in results:
            ranks = ", ".join(str(rank) if rank is not None else "miss" for rank in row["ranks"])
            details.append(f"| {row['id']} | {types[row['id']]} | {ranks} | "
                           f"{row['available']}/{len(row['ranks'])} |")
    (ROOT / "eval/development-bm25-diagnostic.md").write_text(
        "\n".join(report + details) + "\n", encoding="utf-8")
    print("\n".join(report[-3:]))


if __name__ == "__main__":
    main()

