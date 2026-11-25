"""Run the frozen held-out set through the local web app once."""
import hashlib
import json
from time import perf_counter
from urllib.request import Request, urlopen

from evaluate_bm25 import ROOT, read_jsonl

REVIEW = ROOT / "eval/review"
FROZEN = REVIEW / "heldout-frozen.jsonl"
MANIFEST = REVIEW / "heldout-freeze.json"
OUTPUT = ROOT / "eval/heldout-app-outputs.jsonl"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for relative_path, expected in manifest["files"].items():
        if digest(ROOT / relative_path) != expected:
            raise ValueError(f"Frozen artifact changed: {relative_path}")
    items = read_jsonl(FROZEN)
    if len(items) != 20 or any(q["split"] != "heldout" or
                               q["review_status"] != "source_checked" for q in items):
        raise ValueError("Expected 20 frozen, source-checked held-out questions.")
    complete = read_jsonl(OUTPUT) if OUTPUT.exists() else []
    if [r["id"] for r in complete] != [q["id"] for q in items[:len(complete)]]:
        raise ValueError("Checkpoint IDs do not match the frozen questions.")
    for item in items[len(complete):]:
        request = Request("http://127.0.0.1:8000/api/ask",
                          data=json.dumps({"question": item["question"], "mode": "qwen"}).encode(),
                          headers={"Content-Type": "application/json"})
        start = perf_counter()
        with urlopen(request, timeout=200) as response:
            result = json.load(response)
        record = {"id": item["id"], **result, "seconds": round(perf_counter() - start, 2)}
        with OUTPUT.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(item["id"], result["mode"] or "abstained", flush=True)


if __name__ == "__main__":
    main()

