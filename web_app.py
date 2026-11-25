"""Local site and HTTP interface for NIST question answering."""
import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ask_nist import DATA, answer_question, answer_with_local_model, cited_answer
from evaluate_bm25 import BM25, read_jsonl

WEB = Path(__file__).resolve().with_name("web")
app = FastAPI(title="NIST Evidence Desk")
app.mount("/assets", StaticFiles(directory=WEB), name="assets")


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=600)
    mode: Literal["extractive", "qwen"] = "extractive"


@lru_cache(maxsize=1)
def corpus():
    labels = json.loads((DATA / "nist-page-label-map.json").read_text(encoding="utf-8"))
    return labels, read_jsonl(DATA / "chunks-A.jsonl"), BM25(read_jsonl(DATA / "chunks-C.jsonl"))


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(WEB / "index.html")


@app.post("/api/ask")
def ask(request: Question):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Enter a question first.")
    try:
        labels, rows, index = corpus()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail="Run python build_corpus.py first.") from exc

    if request.mode == "qwen":
        try:
            result = answer_with_local_model(question, labels, rows, index)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        if result:
            evidence = [cited_answer(proof["quote"], cite, labels)
                        for proof in result["evidence"] for cite in proof["citations"]]
            return {"answer": result["text"], "sources": evidence, "mode": "qwen"}
    result = answer_question(question, labels, rows, index)
    if result:
        return {"answer": result["text"], "sources": [result], "mode": "extractive"}
    return {"answer": None, "sources": [], "mode": None}
