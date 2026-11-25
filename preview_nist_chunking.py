"""Dry-run chunking strategies using the verified canonical page text."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_nist import validate_chunk_citations

MAX_WORDS = 384
STRATEGIES = ("A", "B", "C")
WORD = re.compile(r"\S+")

HEADING = re.compile(
    r"(?m)^[ \t]*(?:Appendix [A-Z][.:][^\n]*|"
    r"\d+(?:\.\d+){1,3}\.?[ \t]+[A-Z][^\n]*|"
    r"[A-Z]\.\d+(?:\.\d+)*\.[ \t]+[A-Z][^\n]*|"
    r"Executive[ \t]+Summary[ \t]*|"
    r"Part \d+:[^\n]*)$"
)
SENTENCE_BREAK = re.compile(
    r"(?<=[.!?])(?:[”')\]]*)\s+(?=[A-Z“‘])|(?=\n[ \t]*•)|\n[ \t]*\n"
)
NUMBERED_HEADING_PREFIX = re.compile(
    r"[ \t]*(?:\d+(?:\.\d+)*|[A-Z]\.\d+(?:\.\d+)*)\."
)
ABBREVIATION = re.compile(r"(?:\b(?:e\.g|i\.e|et al|Fig|Dr|Mr|Ms|vs|No|U\.S)|\b[A-Z])\.$")
SAMPLE_PAGES = (("600-1", 17), ("100-1", 34), ("600-1", 51))


def word_count(text):
    return len(WORD.findall(text))


def windows(text, limit, overlap=0):
    words = list(WORD.finditer(text))
    for start in range(0, len(words), limit - overlap):
        stop = min(start + limit, len(words))
        yield words[start].start(), words[stop - 1].end()
        if stop == len(words):
            break


def pack(text, units, limit, max_units=None):
    start = end = None
    size = count = 0
    for left, right in units:
        words = word_count(text[left:right])
        if not words:
            continue
        if count and (size + words > limit or count == max_units):
            yield start, end
            start = None
            size = count = 0
        if words > limit:
            for a, b in windows(text[left:right], limit):
                yield left + a, left + b
            continue
        if start is None:
            start = left
        end = right
        size += words
        count += 1
    if count:
        yield start, end


def paragraphs(text):
    start = 0
    for match in re.finditer(r"\n[ \t]*\n(?:[ \t]*\n)*", text):
        yield start, match.start()
        start = match.end()
    yield start, len(text)


def sections_and_rows(text, rows):
    def prose(start, end):
        region = text[start:end]
        boundaries = sorted({0, len(region), *(m.start() for m in HEADING.finditer(region))})
        for left, right in zip(boundaries, boundaries[1:]):
            section = region[left:right]
            for a, b in pack(section, paragraphs(section), 240):
                yield start + left + a, start + left + b, "prose"

    cursor = 0
    for row in rows:
        if "action_id" in row:
            values = [row[key] for key in ("action_id", "suggested_action", "gai_risks")]
        else:
            values = [value for value in row.values() if value]
        rendered = " | ".join(values)
        start = text.find(rendered, cursor)
        if start < 0:
            raise ValueError("Structured row is missing from canonical page text")
        end = start + len(rendered)
        yield from prose(cursor, start)
        if word_count(rendered) > MAX_WORDS:
            raise ValueError("Structured row exceeds the maximum size")
        yield start, end, "row"
        cursor = end

    yield from prose(cursor, len(text))


def sentences(text):
    start = 0
    for match in SENTENCE_BREAK.finditer(text):
        # Avoid splitting on common abbreviations and keep closing punctuation.
        line_start = text.rfind("\n", 0, match.start()) + 1
        before_break = text[line_start:match.start()]
        if NUMBERED_HEADING_PREFIX.fullmatch(before_break):
            continue
        if ABBREVIATION.search(text[max(start, match.start() - 12):match.start()]):
            continue
        end = match.start() + len(match[0]) - len(match[0].lstrip("”')]"))
        yield start, end
        start = match.end()
    yield start, len(text)


def preview(pages, strategy):
    for page in sorted(pages, key=lambda p: (p["report_id"], p["pdf_page"])):
        text = page["text"]
        if strategy == "A":
            spans = sections_and_rows(text, page["rows"])
        elif strategy == "B":
            spans = ((a, b, "window") for a, b in windows(text, 180, 30))
        elif strategy == "C":
            spans = ((a, b, "sentences") for a, b in pack(text, sentences(text), 180, 5))
        else:
            raise ValueError(f"Unknown strategy {strategy!r}")
        for start, end, kind in spans:
            body = text[start:end].strip()
            identity = json.dumps([strategy, page["report_id"], page["pdf_page"], start, end, body],
                                  ensure_ascii=False, separators=(",", ":"))
            digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
            yield dict(id=f"{strategy}-{digest}", text=body, kind=kind,
                       citations=[dict(report_id=page["report_id"], pdf_page=page["pdf_page"])])


def load_pages(directory):
    return [json.loads(line) for line in
            (directory / "nist-pages.jsonl").read_text(encoding="utf-8").splitlines()]


def write_report(directory, destination):
    pages = load_pages(directory)
    labels = json.loads((directory / "nist-page-label-map.json").read_text(encoding="utf-8"))
    page_text = {(page["report_id"], page["pdf_page"]): page["text"] for page in pages}
    results = {strategy: list(preview(pages, strategy)) for strategy in STRATEGIES}
    for chunks in results.values():
        validate_chunk_citations(chunks, labels, page_text)
    lines = [
        "# Chunking proposal and dry-run samples", "",
        "These are measured counts from an in-memory preview of the pinned page records. "
        "The preview uses page boundaries for all strategies. No chunk dataset or retrieval "
        "index is written.", "",
        "| Strategy | Rule | AI 100-1 | AI 600-1 | Total | Largest chunk (words) |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    rules = {
        "A": "Recognized section headings and prose paragraphs, packed to 240 words. Each table row stays whole.",
        "B": "180-word windows with a 30-word overlap between adjacent windows on the same page.",
        "C": "Greedy packs of up to five sentence or list units and 180 words.",
    }
    for strategy, chunks in results.items():
        count = Counter(c["citations"][0]["report_id"] for c in chunks)
        maximum = max(word_count(c["text"]) for c in chunks)
        lines.append(f"| {strategy} | {rules[strategy]} | {count['100-1']} | "
                     f"{count['600-1']} | {len(chunks)} | {maximum} |")
    lines.extend(["", "Sizes count whitespace-delimited words. A uses a 384-word hard ceiling "
                  "so the original table row can stay whole. B and C are capped at 180 words. "
                  "C uses a deterministic punctuation heuristic and falls back to word splitting "
                  "for an individual unit over 180 words.", ""])
    for report, page in SAMPLE_PAGES:
        lines.extend([f"## AI {report} · PDF page {page}", ""])
        for strategy, chunks in results.items():
            matches = [c for c in chunks if c["citations"] ==
                       [dict(report_id=report, pdf_page=page)]]
            # Choose a row-bearing example when available, and the opener for Appendix A.
            markers = {("600-1", 17): "GV-1.1-001 |", ("100-1", 34): "MEASURE 1.1:"}
            marker = markers.get((report, page))
            example = next((c for c in matches if marker and marker in c["text"]), matches[0])
            lines.extend([f"### {strategy} · {len(matches)} on this page · "
                          f"example {word_count(example['text'])} words", "", "~~~~text",
                          example["text"], "~~~~", ""])
    destination.write_text("\n".join(lines), encoding="utf-8")
    return {strategy: len(chunks) for strategy, chunks in results.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(write_report(args.pages_dir, args.report))




