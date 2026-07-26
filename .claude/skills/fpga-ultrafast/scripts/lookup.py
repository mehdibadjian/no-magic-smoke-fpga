#!/usr/bin/env python3
"""Pull specific blocks out of the No Magic Smoke FPGA methodology book.

The book is ~74,000 words. Reading a whole section to answer "what is the
control set rule" costs ~4,300 words of context for about 40 useful ones. This
script extracts just the block you need.

Every section has the same named blocks, so retrieval is structural rather than
semantic:

    Bullet Points            the cheat sheet - commands, thresholds, formulas
    Do the Math              the worked calculation with units and a verdict
    The Real Artifact        complete pasteable XDC / RTL / Tcl / annotated report
    Analogy -> Silicon       metaphor to named primitive mapping
    Code Detective           a realistic bug, and the corrected code
    Sharpen Your Pencil      exercises
    Answers                  full working for every question the section asks
    There Are No Dumb Questions

Usage:
    lookup.py --list
    lookup.py --search "clock domain crossing"
    lookup.py --section 2.3
    lookup.py --section 2.3 --block "Do the Math"
    lookup.py --search metastability --block "Bullet Points"

Exit status is 1 when nothing matched, so callers can branch on it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

BLOCKS = [
    "Analogy → Silicon",
    "Do the Math",
    "The Real Artifact",
    "Code Detective",
    "Sharpen Your Pencil",
    "Answers",
    "There Are No Dumb Questions",
    "Bullet Points",
]

# "Analogy -> Silicon" is easier to type than "Analogy → Silicon".
BLOCK_ALIASES = {
    "analogy": "Analogy → Silicon",
    "analogy -> silicon": "Analogy → Silicon",
    "analogy->silicon": "Analogy → Silicon",
    "math": "Do the Math",
    "artifact": "The Real Artifact",
    "code": "Code Detective",
    "detective": "Code Detective",
    "exercise": "Sharpen Your Pencil",
    "exercises": "Sharpen Your Pencil",
    "pencil": "Sharpen Your Pencil",
    "answers": "Answers",
    "questions": "There Are No Dumb Questions",
    "faq": "There Are No Dumb Questions",
    "cheatsheet": "Bullet Points",
    "cheat sheet": "Bullet Points",
    "summary": "Bullet Points",
    "bullets": "Bullet Points",
}

H1_RE = re.compile(r"^#\s+Section\s+([\d.]+):\s*(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)

SITE = "https://mehdibadjian.github.io/no-magic-smoke-fpga/"


def _sections_under(base: Path) -> Path | None:
    for sub in (base / "docs" / "sections", base / "sections", base):
        if sub.is_dir() and list(sub.glob("[0-9].[0-9]_*.md")):
            return sub
    return None


def find_book_root(explicit: str | None = None) -> Path | None:
    """Locate the directory containing the book's sections.

    An explicitly supplied path is authoritative: if it is wrong, fail rather
    than silently falling back. A caller that names a path and gets answers from
    a different copy of the book has been misled in a way that is very hard to
    notice.

    Otherwise search $NO_MAGIC_SMOKE_ROOT, then the repo this script lives in,
    then every parent of the working directory — the last case matters when the
    skill is installed globally but the book is vendored into the project being
    worked on.
    """
    if explicit:
        found = _sections_under(Path(explicit).expanduser())
        if found is None:
            raise FileNotFoundError(
                f"--book-root {explicit!r} does not contain the book's sections"
            )
        return found

    candidates: list[Path] = []
    if env := os.environ.get("NO_MAGIC_SMOKE_ROOT"):
        candidates.append(Path(env).expanduser())
    # .../.claude/skills/fpga-ultrafast/scripts/lookup.py -> repo root
    candidates.append(Path(__file__).resolve().parents[4])
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    for base in candidates:
        if (found := _sections_under(base)) is not None:
            return found
    return None


def load_sections(root: Path) -> list[dict]:
    sections = []
    for path in sorted(root.glob("[0-9].[0-9]_*.md")):
        text = path.read_text(encoding="utf-8")
        m = H1_RE.search(text)
        sections.append(
            {
                "id": m.group(1) if m else path.stem.split("_")[0],
                "title": m.group(2) if m else path.stem,
                "path": path,
                "text": text,
            }
        )
    return sections


def extract_block(text: str, block: str) -> str | None:
    """Return the body under `### <block>`, up to the next `###`.

    Headings may carry a subtitle ("### Code Detective: The XDC Conflict"), so
    match on the prefix rather than on equality.
    """
    for m in H3_RE.finditer(text):
        heading = m.group(1)
        if heading == block or heading.startswith(block + ":"):
            start = m.start()
            nxt = text.find("\n### ", m.end())
            return text[start:nxt if nxt != -1 else len(text)].strip()
    return None


def resolve_block(name: str) -> str | None:
    key = name.strip().lower()
    if key in BLOCK_ALIASES:
        return BLOCK_ALIASES[key]
    for block in BLOCKS:
        if block.lower() == key or block.lower().startswith(key):
            return block
    return None


def search(sections: list[dict], query: str, limit: int = 5) -> list[tuple[dict, float, list[str]]]:
    """Rank sections for a query.

    Deliberately dumb: no index, no embeddings, no dependencies. The corpus is
    18 files, so brute force is instant and never goes stale.

    Raw term frequency does not work here, though. Every section of an FPGA book
    says "clock" and "design" constantly, so a search for "clock domain
    crossing" would rank the clocking chapter above the CDC chapter purely on
    the word "clock". Terms are therefore weighted by how *rare* they are across
    the corpus, and an exact phrase match outweighs any amount of scattered
    term frequency.
    """
    import math

    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    if not terms:
        return []

    lowered = [(sec, sec["text"].lower()) for sec in sections]
    n = len(sections)

    # log(1 + N/df): a term in every section still counts a little, a term in
    # two sections counts ~3x more.
    idf = {}
    for t in terms:
        df = sum(1 for _, low in lowered if t in low) or 1
        idf[t] = math.log(1 + n / df)

    phrase = query.strip().lower()
    results = []
    for sec, low in lowered:
        score = sum(low.count(t) * idf[t] for t in terms)
        if len(terms) > 1:
            score += 60 * low.count(phrase)
        title = sec["title"].lower()
        score += 25 * sum(idf[t] for t in terms if t in title)
        if score <= 0:
            continue

        hits = []
        for line in sec["text"].splitlines():
            stripped = line.strip()
            if not stripped.startswith(("- ", "**", "###")):
                continue
            ll = stripped.lower()
            if phrase in ll or sum(t in ll for t in terms) >= max(1, len(terms) - 1):
                hits.append(stripped)
            if len(hits) >= 3:
                break
        results.append((sec, score, hits))

    results.sort(key=lambda r: -r[1])
    return results[:limit]


def section_url(sec: dict) -> str:
    return f"{SITE}sections/{sec['path'].stem}/"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Extract blocks from the No Magic Smoke FPGA methodology book.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--search", metavar="QUERY", help="find the sections covering a topic")
    ap.add_argument("--section", metavar="ID", help="section id, e.g. 2.3")
    ap.add_argument(
        "--block",
        metavar="NAME",
        help="which block to print (default: Bullet Points). "
        f"One of: {', '.join(BLOCKS)}",
    )
    ap.add_argument("--full", action="store_true", help="print the whole section")
    ap.add_argument("--list", action="store_true", help="list every section")
    ap.add_argument("--book-root", help="path to the book (default: auto-detect)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    try:
        root = find_book_root(args.book_root)
    except FileNotFoundError as exc:
        print(f"{exc}\n\nUse --list from inside the repo, or read it online:\n  {SITE}",
              file=sys.stderr)
        return 1

    if root is None:
        print(
            "Could not find the book's sections.\n\n"
            "Pass --book-root, set NO_MAGIC_SMOKE_ROOT, or read it online:\n"
            f"  {SITE}\n",
            file=sys.stderr,
        )
        return 1

    sections = load_sections(root)
    if not sections:
        print(f"No section files found under {root}", file=sys.stderr)
        return 1

    if args.list:
        if args.json:
            print(json.dumps(
                [{"id": s["id"], "title": s["title"], "url": section_url(s)} for s in sections],
                indent=2,
            ))
        else:
            print(f"{len(sections)} sections in {root}\n")
            for s in sections:
                print(f"  {s['id']:<5} {s['title']}")
            print(f"\nBlocks available per section: {', '.join(BLOCKS)}")
        return 0

    if args.search:
        hits = search(sections, args.search)
        if not hits:
            print(f"No match for {args.search!r}. Try --list to see the topics covered.")
            return 1

        if args.block:
            # Search, then print the requested block from the best match.
            block = resolve_block(args.block)
            if block is None:
                print(f"Unknown block {args.block!r}. One of: {', '.join(BLOCKS)}", file=sys.stderr)
                return 1
            sec = hits[0][0]
            body = extract_block(sec["text"], block)
            print(f"# Section {sec['id']}: {sec['title']}\n# {section_url(sec)}\n")
            print(body or f"(section {sec['id']} has no '{block}' block)")
            if len(hits) > 1:
                others = ", ".join(f"{s['id']}" for s, _, _ in hits[1:])
                print(f"\n---\nAlso relevant: {others}")
            return 0

        print(f"Sections matching {args.search!r}:\n")
        for sec, score, lines in hits:
            print(f"  {sec['id']:<5} {sec['title']}  (score {score:.0f})")
            print(f"        {section_url(sec)}")
            for line in lines:
                trimmed = line if len(line) <= 100 else line[:97] + "..."
                print(f"        | {trimmed}")
            print()
        print("Next: --section <id> --block 'Bullet Points'  (or 'Do the Math', 'The Real Artifact')")
        return 0

    if args.section:
        wanted = args.section.strip()
        sec = next((s for s in sections if s["id"] == wanted), None)
        if sec is None:
            print(f"No section {wanted!r}. Use --list.", file=sys.stderr)
            return 1

        print(f"# Section {sec['id']}: {sec['title']}")
        print(f"# {section_url(sec)}\n")

        if args.full:
            print(sec["text"])
            return 0

        block = resolve_block(args.block) if args.block else "Bullet Points"
        if block is None:
            print(f"Unknown block {args.block!r}. One of: {', '.join(BLOCKS)}", file=sys.stderr)
            return 1

        body = extract_block(sec["text"], block)
        if body is None:
            print(f"(no '{block}' block in this section)")
            return 1
        print(body)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
