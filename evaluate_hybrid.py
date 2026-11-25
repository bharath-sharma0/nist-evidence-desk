"""Compare reciprocal rank fusion with BM25 and BGE on the NIST pilot."""
import argparse

from evaluate_bm25 import BM25, ROOT, evaluate, read_jsonl

DEPTH = 30
RANK_CONSTANT = 60


def fuse(*rankings, k=5):
    """Reward items ranked highly by either retriever or supported by both."""
    scores = {}
    chunks = {}
    for ranking in rankings:
        for rank, chunk in enumerate(ranking, 1):
            key = chunk["id"]
            chunks[key] = chunk
            scores[key] = scores.get(key, 0.0) + 1 / (RANK_CONSTANT + rank)
    return [chunks[key] for key in sorted(scores, key=lambda key: (-scores[key], key))[:k]]


def main(development=False):
    from evaluate_dense import BGE, PREFIX, REVISION, metrics

    model = BGE(ROOT / "data/bge-small")
    if development:
        source = ROOT / "eval/review/development.jsonl"
        output = ROOT / "eval/development-retrieval-comparison.md"
    else:
        source = ROOT / "eval/questions.jsonl"
        output = ROOT / "eval/hybrid-pilot-results.md"
    items = read_jsonl(source)
    if development and any(q["split"] != "development" for q in items):
        raise ValueError("Expected only development questions")
    questions = [q for q in items if q["evidence"]]
    query_vectors, _ = model.encode([PREFIX + q["question"] for q in questions])
    report = [
        "# Provisional development retrieval comparison" if development else "# Hybrid retrieval pilot", "",
        f"Reciprocal rank fusion uses up to {DEPTH} results per retriever and adds "
        f"1/({RANK_CONSTANT} + rank) for each appearance. A missing candidate contributes zero. "
        f"The same {len(questions)} answerable questions and exact excerpt metric are "
        "used for every row.", "",
        "Development labels remain provisional." if development else "This run uses the pilot.", "",
        f"BGE model revision {REVISION}. BM25 and BGE rankings are regenerated in this run.", "",
        "| Chunking | BM25 evidence Recall@5 | BGE evidence Recall@5 | Hybrid evidence Recall@5 | BM25 complete | BGE complete | Hybrid complete |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    detail = []
    for strategy in "ABC":
        print(f"Encoding strategy {strategy} on CPU...", flush=True)
        chunks = read_jsonl(ROOT / "data/processed" / f"chunks-{strategy}.jsonl")
        keyword = BM25(chunks)
        vectors, _ = model.encode([chunk["text"] for chunk in chunks])
        keyword_hits, dense_hits, fused_hits = {}, {}, {}
        for question, vector in zip(questions, query_vectors):
            query = question["question"]
            keyword_hits[query] = keyword.search(query, DEPTH)
            scores = vectors @ vector
            order = sorted(range(len(chunks)), key=lambda i: (-scores[i], chunks[i]["id"]))[:DEPTH]
            dense_hits[query] = [chunks[i] for i in order]
            fused_hits[query] = fuse(keyword_hits[query], dense_hits[query])
        compared = [evaluate(chunks, questions, ranking.__getitem__) for ranking in
                    ({q: hits[:5] for q, hits in keyword_hits.items()},
                     {q: hits[:5] for q, hits in dense_hits.items()}, fused_hits)]
        scores = [metrics(rows) for rows in compared]
        report.append(f"| {strategy} | " + " | ".join(
            [f"{recall:.1%}" for recall, _ in scores] +
            [f"{complete}/{len(questions)}" for _, complete in scores]) + " |")
        detail.extend(["", f"## Strategy {strategy}", "",
                       "| Question | BM25 ranks | BGE ranks | Hybrid ranks |",
                       "| --- | --- | --- | --- |"])
        for rows in zip(*compared):
            ranks = [", ".join(str(r) if r else "miss" for r in row["ranks"]) for row in rows]
            detail.append(f"| {rows[0]['id']} | " + " | ".join(ranks) + " |")
    report.extend(["", "Complete means all labeled excerpts for a question appear in the top five. "
                   "Abstention and answer generation are outside this pilot."])
    report.extend(detail)
    output.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(line for line in report if line.startswith(("| A ", "| B ", "| C "))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--development", action="store_true")
    main(development=parser.parse_args().development)




