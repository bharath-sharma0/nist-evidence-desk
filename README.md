# NIST Evidence Desk

**[Try the live demo](https://nist-evidence-desk.velvetdove1.chatgpt.site)** · Search selected NIST passages and open their PDF citations.

NIST Evidence Desk is a local question-answering app over two NIST AI risk
management reports. It retrieves passages, returns a source excerpt or a short
answer from Qwen 1.7B, and displays the quoted evidence with a link to its PDF page.
The browser uses plain HTML, CSS, and JavaScript over a FastAPI endpoint.

## Results

| Evaluation | Observed result |
| --- | ---: |
| Best development evidence Recall@5 | 57.3% (BM25 with sentence-based chunks) |
| Correct answers on the frozen held-out set | 7/17 answerable items |
| Correct answers fully supported by the displayed passages | 2/17 answerable items |
| Correct abstentions | 3/3 unanswerable items |
| Correct overall, including abstentions | 10/20 items |
| Software tests | 26 passed |

Development compares BM25, BGE-small, and reciprocal rank fusion over three
chunking strategies. The held-out run measures the browser configuration once,
with local Qwen and an extractive fallback. The labels and answers were checked against the source reports. The sample is small and some questions share source rows.
The software tests cover pipeline behavior and the evaluation files.

[Development retrieval comparison](eval/development-retrieval-comparison.md) ·
[Held-out results and errors](eval/heldout-app-results.md)

## How it works

1. Verify two pinned source PDFs and extract 112 pages. Preserve both the physical
   PDF page and the printed page label.
2. Extract table rows, preserve two-column reading order, and build three chunk
   datasets for comparison.
3. Retrieve evidence for a question using BM25 in the browser app. Compare dense
   BGE and rank fusion in separate evaluation scripts.
4. Return a source excerpt or generate a short Qwen answer. Display cited
   passages beside the answer and use an extractive fallback when no cited
   generated answer survives validation.

## Build the corpus

Run these commands from this directory in your Python 3.12 environment.

```powershell
python -m pip install -r requirements.txt
python build_corpus.py
python -m unittest
```

The builder downloads the two original reports to `data/raw` if needed, verifies their SHA-256 hashes, and writes the page records, footer audit, page-label map, and chunk files to `data/processed`. To reuse existing source PDFs, pass `--source PATH_TO_PDFS`. See the [corpus manifest](nist-corpus-manifest.md) for the pinned editions and attribution notes.

| Dataset | Method | Chunks |
| --- | --- | ---: |
| `chunks-A.jsonl` | Section-aware prose and whole table rows | 488 |
| `chunks-B.jsonl` | 180-word windows with 30 words of overlap | 264 |
| `chunks-C.jsonl` | Up to five sentence or list units, capped at 180 words | 392 |

Each line has a deterministic ID, the exact chunk text, a chunk type, and citations with a report ID and physical PDF page. Look up the printed label in the page-label map. The development comparison measures retrieval against labeled evidence.

Generated data is ignored by Git. The local build is for inspection and evaluation. Review the manifest's source-attribution notes before distributing corpus assets.

## Run the BM25 pilot

Run `python evaluate_bm25.py` after building the corpus. It regenerates the
[pilot results](eval/bm25-pilot-results.md) for all three chunking strategies using
the nine answerable questions. The report records evidence coverage and per-question
ranks. The pilot does not measure generation or abstention.

## Run the dense retrieval pilot

The dense run uses BAAI/bge-small-en-v1.5 on CPU via ONNX Runtime. Run these
commands in PowerShell from the project directory after building the corpus.

```powershell
python -m pip install -r requirements-dense.txt
New-Item -ItemType Directory -Force data/bge-small | Out-Null
$model = 'https://huggingface.co/BAAI/bge-small-en-v1.5/resolve/5c38ec7c405ec4b44b94cc5a9bb96e735b38267a'
curl.exe -fL "$model/tokenizer.json" -o data/bge-small/tokenizer.json
curl.exe -fL "$model/onnx/model.onnx" -o data/bge-small/model.onnx
python evaluate_dense.py
```

The [dense pilot report](eval/dense-pilot-results.md) compares BM25 and BGE
on the same questions and records token lengths before truncation.

| Pinned model file | SHA-256 |
| --- | --- |
| tokenizer.json | d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66 |
| model.onnx | 828e1496d7fabb79cfa4dcd84fa38625c0d3d21da474a00f08db0f559940cf35 |

## Run the hybrid retrieval pilot

After completing the dense setup above, run `python evaluate_hybrid.py`.
The script uses the top 30 candidates from each retriever and combines their
ranks with reciprocal rank fusion (rank constant 60). It regenerates the
[hybrid pilot comparison](eval/hybrid-pilot-results.md).

## Compare retrievers on the development draft

Run `python evaluate_hybrid.py --development` after the dense setup. The
[development comparison](eval/development-retrieval-comparison.md) reports
BM25, dense BGE, and hybrid results on the same answerable development items.
The held-out file is reserved for the frozen evaluation. The pilot reports are snapshots from before the sentence splitter was corrected to preserve numbered headings. The development comparison uses the corrected corpus.


## Generate answers with local Ollama

Install Ollama for Windows and start it. In the project directory, pull the
selected model and run one question in local-model mode.

```bat
ollama pull qwen3:1.7b
python ask_nist.py --local-model "For action GV-1.1-001, which legal areas does NIST specifically mention?"
```

The local-model mode sends the question and five BM25 passages to the Ollama
endpoint on this computer. It checks that each returned quote occurs in the
cited passage before displaying its report and page. Quote validation checks
citation provenance. Human evaluation is still needed to verify that the
generated answer follows from its citations.

## Evaluate local answer generation

With Ollama running and the model available, run `python evaluate_qwen.py`.
The script evaluates the development draft, checkpoints completed questions,
and writes [the answer and citation diagnostic](eval/development-qwen-diagnostic.md).
It does not score the held-out file.

## Open the browser interface

From the project directory in your activated environment, install the web
dependencies and start the server.

```bat
python -m pip install -r requirements-web.txt
python -m uvicorn web_app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. Pick **Quote from the report** for a source excerpt or
**Generate with local Qwen** for a synthesized answer. The Qwen mode requires a
running Ollama service and shows the validated source quote beside the answer.
The server accepts questions at `POST /api/ask` and exposes API docs at `/docs`.

## Held-out browser app evaluation

The frozen 20-question set was evaluated once through the local browser API,
using Qwen with extractive fallback. The
[results](eval/heldout-app-results.md) report strict answer correctness and
visible-source support separately. The
[freeze manifest](eval/review/heldout-freeze.json) identifies the labels and
pipeline files. Run `python score_heldout_app.py` to regenerate the scored
report from the recorded outputs and judgments without querying the model.
