"""Run the pinned BGE-small CPU pilot against the BM25 baseline."""
from time import perf_counter

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

from evaluate_bm25 import BM25, ROOT, evaluate, read_jsonl

REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
PREFIX = "Represent this sentence for searching relevant passages: "
LIMIT = 512


class BGE:
    def __init__(self, directory):
        self.tokenizer = Tokenizer.from_file(str(directory / "tokenizer.json"))
        self.tokenizer.no_truncation()
        self.tokenizer.no_padding()
        options = ort.SessionOptions()
        options.intra_op_num_threads = 4
        self.session = ort.InferenceSession(str(directory / "model.onnx"), options,
                                            providers=["CPUExecutionProvider"])
        self.inputs = [field.name for field in self.session.get_inputs()]

    def encode(self, texts):
        self.tokenizer.no_truncation()
        self.tokenizer.no_padding()
        lengths = [len(encoding.ids) for encoding in self.tokenizer.encode_batch(texts)]
        self.tokenizer.enable_truncation(max_length=LIMIT)
        self.tokenizer.enable_padding()
        vectors = []
        for start in range(0, len(texts), 16):
            batch = self.tokenizer.encode_batch(texts[start:start + 16])
            fields = {
                "input_ids": np.asarray([item.ids for item in batch], dtype=np.int64),
                "attention_mask": np.asarray([item.attention_mask for item in batch], dtype=np.int64),
                "token_type_ids": np.asarray([item.type_ids for item in batch], dtype=np.int64),
            }
            hidden = self.session.run(["last_hidden_state"], {name: fields[name] for name in self.inputs})[0]
            cls = hidden[:, 0, :]
            vectors.append(cls / np.linalg.norm(cls, axis=1, keepdims=True))
        return np.concatenate(vectors), lengths


def metrics(rows):
    hits = [sum(rank is not None for rank in row["ranks"]) for row in rows]
    recall = sum(hit / len(row["ranks"]) for hit, row in zip(hits, rows)) / len(rows)
    complete = sum(hit == len(row["ranks"]) for hit, row in zip(hits, rows))
    return recall, complete


def main():
    model = BGE(ROOT / "data/bge-small")
    questions = [q for q in read_jsonl(ROOT / "eval/questions.jsonl") if q["evidence"]]
    query_vectors, query_lengths = model.encode([PREFIX + q["question"] for q in questions])
    queries = {q["question"]: v for q, v in zip(questions, query_vectors)}
    report = [
        "# BGE-small dense retrieval pilot", "",
        f"BAAI/bge-small-en-v1.5 revision {REVISION}. CPU ONNX inference, "
        "normalized CLS embeddings, cosine similarity and the model's retrieval query prefix.",
        "", "The same nine answerable questions and excerpt-matching metric are used for BM25 "
        "and dense retrieval. These pilot results do not estimate held-out performance.", "",
        "| Chunking | BM25 evidence Recall@5 | Dense evidence Recall@5 | BM25 complete | Dense complete | Chunks over 512 tokens | Max tokens | CPU encoding time |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    details = []
    for strategy in "ABC":
        chunks = read_jsonl(ROOT / "data/processed" / f"chunks-{strategy}.jsonl")
        started = perf_counter()
        vectors, lengths = model.encode([chunk["text"] for chunk in chunks])
        elapsed = perf_counter() - started

        def search(query, k=5):
            scores = vectors @ queries[query]
            ranked = sorted(range(len(chunks)), key=lambda i: (-scores[i], chunks[i]["id"]))[:k]
            return [chunks[i] for i in ranked]

        keyword = evaluate(chunks, questions, BM25(chunks).search)
        dense = evaluate(chunks, questions, search)
        bm_recall, bm_complete = metrics(keyword)
        dense_recall, dense_complete = metrics(dense)
        report.append(
            f"| {strategy} | {bm_recall:.1%} | {dense_recall:.1%} | {bm_complete}/9 | "
            f"{dense_complete}/9 | {sum(n > LIMIT for n in lengths)}/{len(chunks)} | "
            f"{max(lengths)} | {elapsed:.1f} s |"
        )
        details.extend(["", f"## Strategy {strategy}", "",
                        "| Question | BM25 excerpt ranks | Dense excerpt ranks |",
                        "| --- | --- | --- |"])
        for before, after in zip(keyword, dense):
            a = ", ".join(str(r) if r else "miss" for r in before["ranks"])
            b = ", ".join(str(r) if r else "miss" for r in after["ranks"])
            details.append(f"| {before['id']} | {a} | {b} |")
    report.extend(["", f"The longest prefixed question was {max(query_lengths)} tokens.",
                   "Encoding time includes tokenization and excludes model loading."])
    report.extend(details)
    (ROOT / "eval/dense-pilot-results.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(line for line in report if line.startswith(("| A ", "| B ", "| C "))))


if __name__ == "__main__":
    main()

