"""Download the pinned corpus, extract it, and build A/B/C chunk datasets."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from extract_nist import SOURCES, extract, validate_chunk_citations
from preview_nist_chunking import STRATEGIES, preview, word_count, MAX_WORDS


def source_path(directory, report, digest):
    path = directory / f"NIST.AI.{report}.pdf"
    if path.exists():
        content = path.read_bytes()
    else:
        url = f"https://nvlpubs.nist.gov/nistpubs/ai/{path.name}"
        with urlopen(url, timeout=60) as response:
            content = response.read()
    if hashlib.sha256(content).hexdigest() != digest:
        raise ValueError(f"Source hash mismatch for {path.name}")
    if not path.exists():
        path.write_bytes(content)
    return path


def build(source, destination):
    source.mkdir(parents=True, exist_ok=True)
    for report, (digest, _) in SOURCES.items():
        source_path(source, report, digest)
    pages = extract(source, destination)
    labels = json.loads((destination / "nist-page-label-map.json").read_text(encoding="utf-8"))
    text = {(p["report_id"], p["pdf_page"]): p["text"] for p in pages}
    counts = {}
    for strategy in STRATEGIES:
        chunks = list(preview(pages, strategy))
        validate_chunk_citations(chunks, labels, text)
        if len({c["id"] for c in chunks}) != len(chunks):
            raise ValueError(f"Duplicate chunk IDs in strategy {strategy}")
        for c in chunks:
            limit = MAX_WORDS if c["kind"] == "row" else (240 if strategy == "A" else 180)
            if not 1 <= word_count(c["text"]) <= limit:
                raise ValueError(f"Invalid chunk size for {c['id']}")
        path = destination / f"chunks-{strategy}.jsonl"
        staged = path.with_suffix(".jsonl.tmp")
        staged.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks),
                          encoding="utf-8")
        staged.replace(path)
        counts[strategy] = len(chunks)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output), sort_keys=True))
