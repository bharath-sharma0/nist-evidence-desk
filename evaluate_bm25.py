"""Evaluate a BM25 keyword baseline on the labeled NIST pilot."""
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    return TOKEN.findall(text.lower())


class BM25:
    def __init__(self, chunks):
        self.chunks = chunks
        self.lengths = []
        self.postings = defaultdict(list)
        for index, chunk in enumerate(chunks):
            counts = Counter(tokens(chunk["text"]))
            self.lengths.append(sum(counts.values()))
            for term, count in counts.items():
                self.postings[term].append((index, count))
        self.average_length = sum(self.lengths) / len(chunks)

    def search(self, query, k=5):
        scores = defaultdict(float)
        for term, query_count in Counter(tokens(query)).items():
            postings = self.postings.get(term, ())
            if not postings:
                continue
            df = len(postings)
            idf = math.log1p((len(self.chunks) - df + 0.5) / (df + 0.5))
            for index, tf in postings:
                length_norm = 1.2 * (0.25 + 0.75 * self.lengths[index] / self.average_length)
                scores[index] += query_count * idf * (tf * 2.2) / (tf + length_norm)
        ranked = sorted(scores, key=lambda i: (-scores[i], self.chunks[i]["id"]))[:k]
        return [self.chunks[i] for i in ranked]


def normalize(text):
    return " ".join(text.split())


def covers(chunk, evidence):
    return any(c["report_id"] == evidence["report_id"] and c["pdf_page"] == evidence["pdf_page"]
               for c in chunk["citations"]) and normalize(evidence["quote"]) in normalize(chunk["text"])


def evaluate(chunks, questions, search=None):
    if search is None:
        search = BM25(chunks).search
    results = []
    for question in questions:
        evidence = question["evidence"]
        if not evidence:
            continue
        top = search(question["question"])
        first_ranks = [next((rank for rank, chunk in enumerate(top, 1) if covers(chunk, item)), None)
                       for item in evidence]
        available = sum(any(covers(chunk, item) for chunk in chunks) for item in evidence)
        results.append({"id": question["id"], "ranks": first_ranks, "available": available})
    return results


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main():
    questions = read_jsonl(ROOT / "eval/questions.jsonl")
    report = [
        "# BM25 pilot results", "",
        "Fixed BM25 settings k1=1.2 and b=0.75. The same nine answerable pilot "
        "questions are scored on each chunk dataset. An evidence hit requires the "
        "correct report and PDF page plus the entire labeled excerpt in one returned "
        "chunk after whitespace normalization. The three abstention cases are excluded.",
        "",
        "| Chunking | Macro evidence Recall@5 | At least one excerpt | All excerpts | Available anywhere |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    details = []
    for strategy in "ABC":
        chunks = read_jsonl(ROOT / "data/processed" / f"chunks-{strategy}.jsonl")
        rows = evaluate(chunks, questions)
        hits = [sum(rank is not None for rank in row["ranks"]) for row in rows]
        n = len(rows)
        macro = sum(hit / len(row["ranks"]) for hit, row in zip(hits, rows)) / n
        any_hit = sum(hit > 0 for hit in hits)
        all_hit = sum(hit == len(row["ranks"]) for hit, row in zip(hits, rows))
        total = sum(len(row["ranks"]) for row in rows)
        available = sum(row["available"] for row in rows)
        report.append(f"| {strategy} | {macro:.1%} | {any_hit}/{n} | {all_hit}/{n} | {available}/{total} |")
        details.extend(["", f"## Strategy {strategy}", "",
                        "| Question | First rank per labeled excerpt | Available anywhere |",
                        "| --- | --- | ---: |"])
        for row in rows:
            ranks = ", ".join(str(rank) if rank else "miss" for rank in row["ranks"])
            details.append(f"| {row['id']} | {ranks} | {row['available']}/{len(row['ranks'])} |")
    report.extend(["", "Macro recall averages each question's fraction of excerpts found. "
                   "Available anywhere is an upper bound imposed by chunk boundaries. "
                   "These are pilot diagnostics. The final evaluation needs a separate held-out set."])
    report.extend(details)
    output = ROOT / "eval/bm25-pilot-results.md"
    output.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[6:9]))


if __name__ == "__main__":
    main()


