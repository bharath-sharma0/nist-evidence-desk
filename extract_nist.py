import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pdfplumber
import pypdf
from nist_geometry import (action_cells, assert_citation_text, extract_columns,
                           layout_column_check, masked_layout, rmf_table, verify_footer)

SOURCES = {
    "100-1": ("7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1", 48),
    "600-1": ("6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a", 64),
}
SAMPLES = {
    "100-1": {6: "Running header and footer", 15: "Figure caption and bullets",
              27: "GOVERN table", 33: "Continued MAP table", 34: "MEASURE table"},
    "600-1": {5: "Introduction and footnotes", 10: "Confabulation and footnotes",
              17: "Suggested-actions table", 51: "Appendix A two-column list",
              52: "Appendix A two-column continuation"},
}
COMPARE = {("100-1", n) for n in (27, 33, 34)} | {("600-1", n) for n in (17, 51, 52)}



def printed_label(report, page):
    if report == "100-1":
        if page in (4, 5):
            return {4: "i", 5: "ii"}[page]
        return str(page - 5) if 6 <= page <= 47 else None
    return str(page - 4) if page >= 5 else None


def repair_wraps(body, words, positioned):
    def join(match):
        left, indent, right = match.groups()
        previous = body[body.rfind("\n", 0, match.start()) + 1:match.start()]
        if positioned and (abs(len(previous) - len(previous.lstrip()) - len(indent)) > 3
                           or re.search(r" {3,}", previous.strip())):
            return match[0]
        if (left + "-" + right).lower() in words:
            return left + "-" + right
        if (left + right).lower() in words:
            return left + right
        return match[0]
    return re.sub(r"([A-Za-z]{2,})-\n( *)([a-z]{2,})\b", join, body)


def validate_chunk_citations(chunks, labels, page_text):
    chunks = list(chunks)
    for chunk in chunks:
        if not chunk["citations"]:
            raise ValueError(f"Missing citations for {chunk['id']}")
        for citation in chunk["citations"]:
            report = citation["report_id"]
            page = citation["pdf_page"]
            if type(page) is not int or str(page) not in labels.get(report, {}):
                raise ValueError(f"Unknown cited page for {chunk['id']}: {report} PDF page {page}")


    assert_citation_text(chunks, page_text)


def fenced(text, language="text"):
    return f"~~~~{language}\n{text.rstrip()}\n~~~~\n"



def extract(source, output):
    labels, pages, compared, footer_audit = {}, {}, {}, []
    action_groups = []
    appendix_pages = []
    for report, (digest, count) in SOURCES.items():
        path = source / f"NIST.AI.{report}.pdf"
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Unexpected SHA-256 for {path}")
        other = pypdf.PdfReader(path)
        with pdfplumber.open(path, unicode_norm="NFKC") as pdf:
            if len(pdf.pages) != count or len(other.pages) != count:
                raise ValueError(f"Unexpected page count for {path}")
            labels[report] = {}
            for page in pdf.pages:
                n = page.page_number
                key = report, n
                label, footer, footer_box = verify_footer(page, report, printed_label(report, n))
                labels[report][str(n)] = label
                footer_audit.append(dict(report_id=report, pdf_page=n, extracted_footer=footer,
                                         printed_page=label))
                raw = page.extract_text(layout=True, x_tolerance=2) or ""
                record = dict(report_id=report, pdf_page=n, printed_page=label,
                              extractor="pdfplumber", raw=raw, rows=[], regions=[])
                pages[key] = record
                regions = []
                if report == "100-1":
                    table = rmf_table(page)
                    if table:
                        box, rows = table
                        record["rows"] = rows
                        regions.append((box, "rmf", rows))
                else:
                    for table in sorted(page.find_tables(), key=lambda t: t.bbox[1]):
                        rows, tasks = action_cells(table)
                        if rows or tasks:
                            regions.append((table.bbox, "gai", (rows, tasks)))
                            record["rows"].extend(rows)
                            action_groups.append((n, rows, tasks))
                    columns = extract_columns(page)
                    if columns:
                        box, left, right = columns
                        appendix_pages.append(n)
                        regions.append((box, "columns", (left, right)))
                if key in COMPARE or (report == "100-1" and regions):
                    alternative = unicodedata.normalize(
                        "NFKC", other.pages[n - 1].extract_text(extraction_mode="layout")
                    )
                    compared[key] = raw, alternative

                # Extract prose between the disjoint table and list bands.
                boxes = [region[0] for region in regions] + [footer_box]
                def prose(top, bottom):
                    cropped = page.crop((0, top, page.width, bottom or page.height))
                    return masked_layout(cropped, boxes, report).strip("\n")
                cursor = 0
                for box, kind, content in sorted(regions, key=lambda item: item[0][1]):
                    if box[1] > cursor:
                        record["regions"].append(("prose", prose(cursor, box[1])))
                    record["regions"].append((kind, content))
                    cursor = box[3]
                record["regions"].append(("prose", prose(cursor, None)))
                page.close()

    pending = []
    for n, rows, tasks in action_groups:
        pending.extend(rows)
        if len({row["action_id"].replace("GV4.3--001", "GV-4.3-001").rsplit("-", 1)[0] for row in pending}) > 1:
            raise ValueError(f"Action group changed before actor tasks on PDF page {n}")
        if tasks:
            for row in pending:
                row["actor_tasks"] = tasks
            pending.clear()
    if pending:
        raise ValueError("Action rows without a closing actor-task entry")

    words = {"environment", "however", "engagement", "implementation", "regularly",
             "re-evaluated", "red-teaming", "risk-based", "non-generative", "pre-deployment"}
    for record in pages.values():
        words.update(word.lower() for word in re.findall(
            r"\b[A-Za-z]+(?:-[A-Za-z]+)*\b", record["raw"]
        ))
    results = []
    samples = ["# Parsed NIST pages\n",
               "Table cells are serialized separately from layout text. Actor tasks at the end "
               "of a continued table apply to all its rows. The page text includes the task line "
               "only on the page where it is printed.\n"]
    for (report, n), record in pages.items():
        label = record["printed_page"]
        parts, prose_parts = [], []
        for kind, content in record.pop("regions"):
            if kind == "prose":
                value = repair_wraps(content, words, False).strip()
                prose_parts.append(value)
            elif kind == "columns":
                value = "\n\n".join(repair_wraps(column, words, False) for column in content)
            elif kind == "rmf":
                for row in content:
                    for field, cell in row.items():
                        if cell:
                            row[field] = " ".join(repair_wraps(cell, words, False).split())
                value = "\n".join(" | ".join(v for v in row.values() if v) for row in content)
            else:
                rows, tasks = content
                value = "\n".join(" | ".join(row[field] for field in
                                  ("action_id", "suggested_action", "gai_risks")) for row in rows)
                if tasks:
                    value = f"{value}\nAI Actor Tasks: {tasks}".strip()
            if value.strip():
                parts.append(value)
        record["layout_text"] = "\n\n".join(p for p in prose_parts if p.strip())
        record["text"] = "\n\n".join(parts)
        raw = record.pop("raw")
        results.append(record)
        if n in SAMPLES[report] or (report == "600-1" and n in (18, 19)):
            title = SAMPLES[report].get(n, "Continued suggested-actions table")
            samples.extend([f"## AI {report} · PDF page {n} · printed page {label}\n",
                            f"{title}\n", fenced(record["text"])])
            if record["rows"]:
                samples.extend(["Named rows\n", fenced(json.dumps(
                    record["rows"], ensure_ascii=False, indent=2
                ), "json")])
        if (report, n) == ("100-1", 6):
            cleanup = "\n".join(["# Before and after · AI 100-1 PDF page 6\n",
                                 "## Before\n", fenced(raw), "## After\n", fenced(record["text"])])

    comparison = ["# Extractor comparison\n",
                  "AI 100-1 table layout outputs are shown against the cells clipped by PDF "
                  "coordinates. The left region is x=90–201 points and the right is "
                  "x=201–523 points. Both layout modes retain the two columns visually but "
                  "return the cells as lines of text separated by whitespace. Clipping gives "
                  "each record a category and subcategories field without interleaving.\n",
                  f"GenAI appendix coordinate splits detected on PDF pages {appendix_pages}.\n"]
    for (report, n), (primary, secondary) in compared.items():
        comparison.extend([f"## AI {report} · PDF page {n}\n",
                           "### pdfplumber layout\n", fenced(primary),
                           "### pypdf layout\n", fenced(secondary)])
        if report == "100-1" and pages[report, n]["rows"]:
            for tool, layout in (("pdfplumber", primary), ("pypdf", secondary)):
                anchors, misplaced = layout_column_check(layout)
                comparison.append(f"{tool} placed {anchors - misplaced} of {anchors} ID anchors "
                                  "in the expected column.\n")
            comparison.extend(["### Selected coordinate cells\n", fenced(json.dumps(
                pages[report, n]["rows"], ensure_ascii=False, indent=2
            ), "json")])
    output.mkdir(parents=True, exist_ok=True)
    for name, content in {
        "nist-page-label-map.json": json.dumps(labels, indent=2) + "\n",
        "nist-footer-audit.json": json.dumps(footer_audit, indent=2) + "\n",
        "nist-parsed-samples.md": "\n".join(samples),
        "nist-cleanup-example.md": cleanup,
        "nist-extractor-comparison.md": "\n".join(comparison),
        "nist-pages.jsonl": "".join(json.dumps(record, ensure_ascii=False) + "\n"
                                    for record in results),
    }.items():
        (output / name).write_text(content, encoding="utf-8")
    return results


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--source", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    print(f"Extracted {len(extract(args.source, args.output))} pages.")





