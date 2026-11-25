# NIST RAG corpus source manifest

Verified 2026-11-25. Each official URL returned HTTP 200 and application/pdf twice. The two downloads of each file had matching SHA-256 hashes. Publication dates are distinct from embedded PDF modification timestamps.

| Report | Published edition | PDF modification timestamp | PDF pages | Bytes | SHA-256 |
| --- | --- | --- | ---: | ---: | --- |
| [NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) | AI RMF 1.0, January 2023 | 2025-06-04T13:01:45-04:00 | 48 | 1946127 | 7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1 |
| [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Generative AI Profile, July 2024 | 2025-03-24T15:11:27-04:00 | 64 | 1174643 | 6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a |

## Attribution review

Searched page-level text, front matter, captions, and footnotes for copyright, permission, and source or adaptation markers. This review covers visible text credits and does not establish underlying rights for every embedded asset.

- **AI 100-1**. Figure 2 credits an OECD adaptation (PDF page 15, printed page 10). Definitions quoted or adapted from OECD or ISO appear on PDF pages 6, 9, 12, 13, 18, and 19. PDF page 9 also credits federal OMB Circular A-130.
- **AI 600-1**. The front matter points to NIST copyright and licensing policy (PDF page 3). No separately marked third-party copyright or image credit surfaced in the text review. The report includes attributed material, including a definition derived from a White House roadmap (PDF page 13, printed page 9).
- For the first public corpus, fetch originals from NIST and omit seals, artwork, and identified OECD/ISO excerpts from redistributed corpus assets pending item-level review. Retain NIST attribution and page references for included text.

[NIST reuse policy](https://www.nist.gov/copyrights-disclaimers)

## Parsing checkpoint

Extracted 112 PDF pages with pdfplumber in layout mode. Candidate metadata includes report ID, physical PDF page, printed page, and section. Layout output retains line wraps, table continuations, and footnotes. Embedded images are outside this text extraction. No chunks were created.

## Reproducible extraction

- Primary extractor is pdfplumber 0.11.9 with NFKC normalization, layout mode, and x_tolerance=2. RMF table cells use printed horizontal rules and x=201 points as the column boundary. GenAI suggested-action tables use pdfplumber's default line-based table cells. pypdf 6.21.4 in layout mode is the comparison extractor.
- Both layout extractors put 91 of 91 identifier anchors in the expected column across 11 RMF table pages. That diagnostic checks the initial ID positions. The selected coordinate extraction also separates the wrapped cell bodies.
- The parallel-bullet detector found GenAI Profile PDF pages 51 and 52. It extracts the list left then right at x=344 points, leaving surrounding full-width prose in order.
- Suggested-action rows carry action_id, suggested_action, gai_risks and actor_tasks. Empty padding cells are dropped. The closing actor-task entry applies to the entire logical table, including rows on the previous page. Canonical page text includes the task line on its printed source page only. The publisher's GV4.3--001 spelling is preserved.
- Every page is checked against its actual extracted footer before saving the map. The map uses one-based physical PDF pages as keys and visible printed labels as values. Unnumbered pages have null labels. A discrepancy aborts extraction.
- The page JSONL stores masked layout text, structured rows, and canonical citation text. Headers, footers, and structured table regions are excluded from layout text. Verified hyphenated word breaks are repaired conservatively.
- The outputs are inspection artifacts and include attributed source text. The redistribution notes above apply to a future public corpus.

Run from the directory containing the two Python modules and the test. Replace the source path with the directory containing the pinned source PDFs.

~~~~powershell
python -m pip install pdfplumber==0.11.9 pypdf==6.21.4
python extract_nist.py --source PATH_TO_PDFS --output .
python test_nist_citations.py
~~~~

Seven tests passed on the regenerated artifacts. The citation validator checks page existence and requires the chunk's text to be a contiguous, whitespace-normalized span of the cited pages in citation order. Tests include real text from a two-page table continuation and reject reversed citations. No corpus chunks were generated.

## Chunking preview

The preview reads the verified page JSONL and writes a Markdown report with counts and nine examples. It keeps previews in memory and does not write a chunk dataset. Run from the output directory with the existing page records.

~~~~powershell
python preview_nist_chunking.py --pages-dir . --report nist-chunking-preview.md
python -m unittest discover -p 'test_nist_*.py'
~~~~
