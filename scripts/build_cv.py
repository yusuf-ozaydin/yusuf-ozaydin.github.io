#!/usr/bin/env python3
"""Build the CV page body from spreadsheet data.

Pipeline:
  1. If scripts/cv_config.json has a non-empty "sheet_id", download each tab of the
     Google Sheet as CSV and overwrite the matching data/cv/<tab>.csv. The sheet must
     be published to the web (File > Share > Publish to web) or shared as "anyone with
     the link can view". Any network/parse failure is logged and skipped -- the
     last-good local CSVs are kept so the site still builds. Pass --strict to make
     failures fatal.
  2. Read every data/cv/*.csv and render _cv/body.md (committed, included by cv.qmd).

In list fields (bullets, education notes, project links) items may be separated by
" | " or by real newlines (Alt+Enter in a Google Sheets cell); either works.

Standard library only. Run from the repo root:  python scripts/build_cv.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "cv"
CONFIG = ROOT / "scripts" / "cv_config.json"
OUT = ROOT / "_cv" / "body.md"

# Bullets within a cell may be separated by " | " or by real newlines (Alt+Enter
# in Google Sheets), so either works when editing the source.
BULLET_SPLIT = re.compile(r"\s*(?:\||\r?\n)\s*")
LINK_SEP = "::"

GVIZ = ("https://docs.google.com/spreadsheets/d/{id}/gviz/tq"
        "?tqx=out:csv&headers=1&sheet={tab}")
PUBHTML = "https://docs.google.com/spreadsheets/d/e/{id}/pubhtml"
PUB_CSV = ("https://docs.google.com/spreadsheets/d/e/{id}/pub"
           "?gid={gid}&single=true&output=csv")
_PUSH_RE = re.compile(r'items\.push\(\{name: "([^"]+)",[^}]*?gid: "(\d+)"')

STRICT = "--strict" in sys.argv[1:]
NO_FETCH = "--no-fetch" in sys.argv[1:]  # rebuild from local data/cv/*.csv only


def log(msg: str) -> None:
    print(f"[build_cv] {msg}")


def fail(msg: str) -> None:
    if STRICT:
        raise SystemExit(f"[build_cv] ERROR: {msg}")
    log(f"WARNING: {msg} (keeping existing local data)")


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "cv-bot"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_source(raw: str) -> tuple[str, str]:
    """Return ('published', pubId) or ('sheet', sheetId) from a URL or bare id."""
    raw = raw.strip()
    m = re.search(r"/d/e/(2PACX-[\w-]+)", raw)
    if m:
        return ("published", m.group(1))
    m = re.search(r"/d/([A-Za-z0-9_-]{20,})", raw)
    if m:
        return ("sheet", m.group(1))
    if raw.startswith("2PACX-"):
        return ("published", raw)
    return ("sheet", raw)


def _write_csv(tab: str, raw: str) -> None:
    if raw.lstrip()[:1] == "<" or "google.visualization" in raw[:200]:
        fail(f"tab '{tab}' did not return CSV (check the sheet is published and the "
             f"tab is named exactly '{tab}')")
        return
    rows = _trim(list(csv.reader(io.StringIO(raw))))
    if len(rows) < 2:
        fail(f"tab '{tab}' has no data rows")
        return
    dest = DATA_DIR / f"{tab}.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    log(f"updated {dest.relative_to(ROOT)} ({len(rows) - 1} rows)")


# --------------------------------------------------------------------------- #
# Step 1: refresh CSVs from the Google Sheet (optional)
# --------------------------------------------------------------------------- #
def refresh_from_sheet() -> None:
    if NO_FETCH:
        log("--no-fetch: building from local data/cv/*.csv without touching the sheet")
        return

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    src = (cfg.get("sheet") or cfg.get("sheet_id") or "").strip()
    tabs = cfg.get("tabs") or [p.stem for p in sorted(DATA_DIR.glob("*.csv"))]

    if not src:
        log("no sheet configured -- building from local data/cv/*.csv")
        return

    kind, ident = parse_source(src)
    log(f"fetching {len(tabs)} tab(s) from {kind} sheet {ident}")

    try:
        if kind == "published":
            html = _get(PUBHTML.format(id=ident))
            gids = dict(_PUSH_RE.findall(html))
            if not gids:
                fail("could not read the tab list from the published sheet")
                return
            for tab in tabs:
                gid = gids.get(tab)
                if gid is None:
                    fail(f"no tab named '{tab}' in the published sheet "
                         f"(found: {', '.join(sorted(gids)) or 'none'})")
                    continue
                _write_csv(tab, _get(PUB_CSV.format(id=ident, gid=gid)))
        else:
            for tab in tabs:
                url = GVIZ.format(id=ident, tab=urllib.request.quote(tab))
                _write_csv(tab, _get(url))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        fail(f"could not reach the sheet: {exc}")
    except Exception as exc:  # noqa: BLE001 - never let a fetch error kill the build
        fail(f"unexpected error fetching the sheet: {exc}")


def _trim(rows: list[list[str]]) -> list[list[str]]:
    """Drop fully empty trailing rows and columns (Sheets exports add them)."""
    rows = [r for r in rows if any((c or "").strip() for c in r)]
    if not rows:
        return rows
    width = max(len(r) for r in rows)
    while width > 1 and all(len(r) < width or not (r[width - 1] or "").strip()
                            for r in rows):
        width -= 1
    return [r[:width] for r in rows]


# --------------------------------------------------------------------------- #
# Step 2: render _cv/body.md
# --------------------------------------------------------------------------- #
def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return [
            {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(fh)
        ]


def by_sort(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    def key(r: dict[str, str]) -> tuple[float, str]:
        raw = (r.get("sort", "") or "").strip()
        try:
            return (float(raw), "")  # tolerate "1", "1.0", "10"
        except ValueError:
            return (9999.0, raw)

    return sorted(rows, key=key)


_WS = re.compile(r"\s+")


def ws(s: str) -> str:
    """Collapse runs of whitespace (incl. stray newlines from Sheets cells)."""
    return _WS.sub(" ", (s or "")).strip()


def split_items(text: str) -> list[str]:
    return [ws(b) for b in BULLET_SPLIT.split(text or "") if b.strip()]


def txt(s: str) -> str:
    """Collapse whitespace, then escape for HTML body text."""
    return escape(ws(s), quote=False)


PLACEHOLDER_DATES = {"", "date unknown", "unknown", "tbd", "n/a", "-"}


def render_bullets(text: str) -> str:
    items = split_items(text)
    if not items:
        return ""
    lis = "\n".join(f"    <li>{txt(b)}</li>" for b in items)
    return f"  <ul>\n{lis}\n  </ul>\n"


def render_links(text: str) -> str:
    out = []
    for chunk in split_items(text):
        if LINK_SEP not in chunk:
            continue
        label, url = (s.strip() for s in chunk.split(LINK_SEP, 1))
        out.append(
            f'<a class="btn btn-sm btn-outline-primary" target="_blank" '
            f'rel="noopener noreferrer" href="{escape(url, quote=True)}">'
            f"{escape(label)}</a>"
        )
    if not out:
        return ""
    return '<div class="project-links">\n  ' + "\n  ".join(out) + "\n</div>\n"


def entry(head: str, dates: str, sub: str, body: str) -> str:
    show_dates = dates.strip().lower() not in PLACEHOLDER_DATES
    dates_html = f'<span class="cv-dates">{txt(dates)}</span>' if show_dates else ""
    sub_html = f'<div class="cv-sub">{txt(sub)}</div>\n' if sub else ""
    return (
        '<div class="cv-entry">\n'
        f'  <div class="cv-head"><span>{txt(head)}</span>{dates_html}</div>\n'
        f"  {sub_html}"
        f"{body}"
        "</div>\n"
    )


def section(title: str, blocks: list[str]) -> str:
    blocks = [b for b in blocks if b.strip()]
    if not blocks:
        return ""
    return f"## {title}\n\n" + "\n".join(blocks) + "\n"


def link(label: str, url: str) -> str:
    attrs = ""
    if url.startswith(("http://", "https://")):
        attrs = ' target="_blank" rel="noopener noreferrer"'
    return f'<a{attrs} href="{escape(url, quote=True)}">{txt(label)}</a>'


def build_header() -> str:
    p = {r.get("key", ""): r.get("value", "") for r in read_csv("profile")}
    if not p:
        return ""

    contact = []
    if p.get("location"):
        contact.append(txt(p["location"]))
    if p.get("email"):
        contact.append(link(p["email"], f'mailto:{p["email"]}'))
    if p.get("linkedin"):
        contact.append(link("LinkedIn", p["linkedin"]))
    if p.get("github"):
        contact.append(link("GitHub", p["github"]))
    if p.get("citizenship"):
        contact.append(txt(p["citizenship"]))

    out = ['<div class="cv-header">']
    headline = p.get("headline", "")
    pron = p.get("pronouns", "")
    if headline:
        h = txt(headline)
        if pron:
            h += f' <span class="pronouns">({txt(pron)})</span>'
        out.append(f'  <p class="cv-headline">{h}</p>')
    if contact:
        out.append(f'  <p class="cv-contact">{" · ".join(contact)}</p>')
    if p.get("summary"):
        out.append(f'  <p class="cv-summary">{txt(p["summary"])}</p>')
    out.append("</div>\n")
    return "\n".join(out)


def build_body() -> str:
    parts: list[str] = []

    parts.append(build_header())

    synced = date.today().strftime("%-d %B %Y")
    parts.append(
        f'::: {{.cv-synced}}\nLast synced {synced}.\n:::\n'
    )

    # Education
    edu_blocks = []
    for r in by_sort(read_csv("education")):
        head = r.get("institution", "")
        sub_bits = [b for b in (r.get("credential", ""), r.get("location", "")) if b]
        gpa = r.get("gpa", "")
        if gpa:
            sub_bits.append(f"GPA {gpa}")
        edu_blocks.append(
            entry(head, r.get("dates", ""), " · ".join(sub_bits),
                  render_bullets(r.get("notes", "")))
        )
    parts.append(section("Education", edu_blocks))

    # Experience
    exp_blocks = []
    for r in by_sort(read_csv("experience")):
        sub_bits = [b for b in (r.get("role", ""), r.get("location", "")) if b]
        exp_blocks.append(
            entry(r.get("organization", ""), r.get("dates", ""),
                  " · ".join(sub_bits), render_bullets(r.get("bullets", "")))
        )
    parts.append(section("Experience", exp_blocks))

    # Projects & Research
    proj_blocks = []
    for r in by_sort(read_csv("projects")):
        body = render_bullets(r.get("bullets", "")) + render_links(r.get("links", ""))
        proj_blocks.append(
            entry(r.get("name", ""), r.get("dates", ""), r.get("role", ""), body)
        )
    parts.append(section("Projects & Research", proj_blocks))

    # Skills
    skill_lines = []
    for r in by_sort(read_csv("skills")):
        cat, items = r.get("category", ""), r.get("items", "")
        if cat and items:
            skill_lines.append(f"<p><strong>{txt(cat)}:</strong> {txt(items)}</p>")
    parts.append(section("Skills", ["\n".join(skill_lines)] if skill_lines else []))

    # Leadership & Activities
    act_blocks = []
    for r in by_sort(read_csv("activities")):
        desc = r.get("description", "")
        body = f"  <p>{txt(desc)}</p>\n" if desc else ""
        act_blocks.append(
            entry(r.get("title", ""), r.get("dates", ""), r.get("role", ""), body)
        )
    parts.append(section("Leadership & Activities", act_blocks))

    return "\n".join(p for p in parts if p.strip()) + "\n"


def main() -> None:
    refresh_from_sheet()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_body(), encoding="utf-8")
    log(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
