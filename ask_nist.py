"""Answer NIST questions with an extracted passage and page citation."""
import argparse
import json
import re

from answer_extractive import answer_in_plain_english
from answer_ollama import generate
from evaluate_bm25 import BM25, ROOT, read_jsonl

ACTION_ID = re.compile(r"\b[A-Z]{2}-\d+\.\d+-\d{3}\b", re.IGNORECASE)
DATA = ROOT / "data/processed"
RISK_QUESTION = re.compile(r"\b(?:risk labels|risk categories|GAI risks)\b", re.IGNORECASE)
RECOMMENDATION_QUESTION = re.compile(
    r"\b(?:legal areas|suggested action|recommend(?:ed|ation|ations|s)?|"
    r"ask(?:s)? teams to do|should be prepared)\b", re.IGNORECASE
)
OUTSIDE_ROW = re.compile(
    r"\b(?:waiver|form number|actor tasks|budget|deadline|"
    r"how many|what percentage|how much)\b", re.IGNORECASE
)


def cited_answer(text, cite, page_labels):
    report, page = cite["report_id"], cite["pdf_page"]
    label = page_labels[report][str(page)]
    printed = f" (printed page {label})" if label is not None else ""
    return {
        "text": text,
        "citation": f"NIST AI {report}, PDF page {page}{printed}",
        "url": f"https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.{report}.pdf#page={page}",
    }


def answer_action(question, index, page_labels):
    action_ids = {match.group().upper() for match in ACTION_ID.finditer(question)}
    if len(action_ids) != 1:
        return None
    if OUTSIDE_ROW.search(question):
        return None
    if RISK_QUESTION.search(question) and not RECOMMENDATION_QUESTION.search(question):
        field = 2
    elif RECOMMENDATION_QUESTION.search(question) and not RISK_QUESTION.search(question):
        field = 1
    else:
        return None
    action = action_ids.pop()
    for chunk in index.search(question, k=5):
        for line in chunk["text"].splitlines():
            fields = line.strip().split(" | ", maxsplit=2)
            if len(fields) == 3 and fields[0] == action:
                return cited_answer(fields[field], chunk["citations"][0], page_labels)
    return None


def answer_question(question, labels, action_chunks=None, plain_index=None):
    match = ACTION_ID.search(question)
    if match:
        action = match.group().upper()
        if action_chunks is None:
            action_chunks = read_jsonl(DATA / "chunks-A.jsonl")
        rows = [c for c in action_chunks if c["kind"] == "row" and
                c["text"].startswith(f"{action} | ")]
        return answer_action(question, BM25(rows), labels) if rows else None

    if plain_index is None:
        plain_index = BM25(read_jsonl(DATA / "chunks-C.jsonl"))
    answer = answer_in_plain_english(question, plain_index)
    return cited_answer(*answer, labels) if answer else None


def answer_with_local_model(question, labels, action_chunks=None, plain_index=None,
                            *, generate_answer=generate):
    if re.search(r"\b(?:waiver|form number)\b", question, re.IGNORECASE):
        return None
    if plain_index is None:
        plain_index = BM25(read_jsonl(DATA / "chunks-C.jsonl"))
    hits = plain_index.search(question, k=5)
    action = ACTION_ID.search(question)
    if action:
        if action_chunks is None:
            action_chunks = read_jsonl(DATA / "chunks-A.jsonl")
        prefix = action.group().upper() + " | "
        exact = next((row for row in action_chunks
                      if row["kind"] == "row" and row["text"].startswith(prefix)), None)
        if exact:
            direct = answer_action(question, BM25([exact]), labels)
            hits = ([dict(exact, text=direct["text"], source_context=exact["text"])] if direct else [exact, *hits[:4]])
    return generate_answer(question, hits)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--local-model", action="store_true", help="Generate an answer with local Ollama")
    args = parser.parse_args()
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    if args.local_model:
        try:
            generated = answer_with_local_model(args.question, labels)
        except RuntimeError as exc:
            parser.exit(1, f"{exc}\n")
        if generated:
            print(generated["text"])
            for citation in generated["citations"]:
                source = cited_answer("", citation, labels)
                print(source["citation"])
                print(source["url"])
            return
        result = None
    else:
        result = answer_question(args.question, labels)
    if result:
        print(result["text"])
        print(result["citation"])
        print(result["url"])
    else:
        print("I couldn't find a source passage that answers the question.")


if __name__ == "__main__":
    main()











