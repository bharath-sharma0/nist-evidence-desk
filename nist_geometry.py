"""Geometry-based checks and table parsing for the pinned NIST PDFs."""
import re

ACTION = re.compile(r"^[A-Z]{2}-\d+\.\d+-\d{3}$")
ACTOR = "AI Actor Tasks:"
COLUMN_SPLIT = 344


def verify_footer(page, report, expected):
    # Report-specific footer bands measured on the pinned page geometry.
    top = 700 if report == "100-1" else 734
    band = page.crop((0, top, page.width, page.height))
    footer = (band.extract_text(x_tolerance=2) or "").strip()
    match = re.fullmatch(r"(?:Page\s*)?(\d+|[ivxlcdm]+)", footer)
    observed = match[1] if match else None
    if observed != expected or (footer and not match):
        raise ValueError(
            f"AI {report} PDF page {page.page_number}: expected footer {expected!r}, found {footer!r}"
        )
    return observed, footer, band.bbox


def extract_columns(page):
    """Find parallel bulleted lists by their duplicated left margin."""
    bullets = [c for c in page.chars if c["text"] == "•"]
    right = [c for c in bullets if 344 < c["x0"] < 349]
    left = [c for c in bullets if 77 < c["x0"] < 82]
    if len(right) < 2 or not any(abs(l["top"] - r["top"]) < 3 for l in left for r in right):
        return None
    first = min(c["top"] for c in left + right)
    last = max(c["bottom"] for c in left + right)
    # Include continuation lines beneath the last bullet, stopping before body prose.
    bounds = (0, first - 3, page.width, last + 10)
    left_text = text_in(page.crop((0, bounds[1], COLUMN_SPLIT, bounds[3])))
    right_text = text_in(page.crop((COLUMN_SPLIT, bounds[1], page.width, bounds[3])))
    return bounds, left_text, right_text


def text_in(page):
    return page.extract_text(x_tolerance=2) or ""


def flatten(text):
    return " ".join(text.split())


def rmf_table(page):
    """Recover RMF cells using the printed horizontal rules and the column gutter."""
    rules = sorted({round(e["top"], 2) for e in page.horizontal_edges
                    if abs(e["x0"] - 201) < 3 and abs(e["x1"] - 522) < 3})
    if len(rules) < 3:
        return None
    rows = []
    for top, bottom in zip(rules[1:], rules[2:]):
        category = text_in(page.crop((90, top, 201, bottom))).strip()
        if not category:
            # Some continued pages omit the repeated category.
            category = None
        actions = text_in(page.crop((201, top, 523, bottom)))
        if not actions.strip():
            raise ValueError(f"Missing RMF subcategory cell on page {page.page_number}")
        rows.append({"category": category, "subcategories": actions.strip()})
    return (89, rules[0] - 0.25, 524, rules[-1] + 0.25), rows


def action_cells(table):
    """Remove padding and retain action rows and table-level actor tasks."""
    actions, tasks = [], None
    for row in table.extract():
        cells = [flatten(cell) for cell in row if cell and cell.strip()]
        if not cells:
            continue
        if ACTION.fullmatch(cells[0]) or cells[0] == "GV4.3--001":
            if len(cells) != 3:
                raise ValueError(f"Expected three populated cells for {cells[0]}: {cells!r}")
            actions.append(dict(action_id=cells[0], suggested_action=cells[1], gai_risks=cells[2]))
        if cells[0].startswith((ACTOR, "AI Actors:")):
            tasks = flatten(" ".join(cells).split(":", 1)[1])
    return actions, tasks


def masked_layout(page, boxes, report):
    def keep(obj):
        if obj.get("object_type") != "char":
            return True
        x = (obj["x0"] + obj["x1"]) / 2
        y = (obj["top"] + obj["bottom"]) / 2
        if report == "100-1" and obj["top"] < 55:
            # The running header occurs only on numbered body pages.
            if 4 < page.page_number < 48:
                return False
        return not any(x0 <= x <= x1 and top <= y <= bottom for x0, top, x1, bottom in boxes)
    return (page.filter(keep).extract_text(layout=True, x_tolerance=2) or "").rstrip()


def normalized(text):
    return flatten(text)


def assert_citation_text(chunks, page_text):
    """Require an exact whitespace-normalized span in the pages cited in order."""
    for chunk in chunks:
        actual = normalized(chunk["text"])
        cited = " ".join(normalized(page_text[c["report_id"], c["pdf_page"]])
                         for c in chunk["citations"])
        if not actual or actual not in cited:
            raise ValueError(f"Chunk text absent from cited pages: {chunk['id']}")




def layout_column_check(raw):
    """Count misplaced category and subcategory ID anchors in a layout rendering."""
    lines = raw.splitlines()
    heading = next(line for line in lines if re.search(r"Categories\s+Subcategories", line))
    left = heading.index("Categories")
    right = heading.index("Subcategories")
    divider = (left + right) // 2
    anchors = [m for line in lines for m in re.finditer(
        r"\b(?:GOVERN|MAP|MEASURE|MANAGE)\s*\d+(\.\s*\d+)?\s*:", line
    )]
    misplaced = sum((m.start() >= divider) != bool(m[1]) for m in anchors)
    return len(anchors), misplaced
