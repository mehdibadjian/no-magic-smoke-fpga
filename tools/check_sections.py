#!/usr/bin/env python3
"""Enforce the authoring contract in AUTHORING.md against docs/sections/*.md.

The first generation pass produced eighteen sections in a convincing Head First
voice with none of the Head First machinery: questions with no answers, toy code
snippets instead of usable artifacts, and not one worked calculation. Nothing
checked for any of that, so nothing caught it.

This script is that check. Run it locally before pushing:

    python3 tools/check_sections.py

Exit status is non-zero when any section violates the contract.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO / "authoring" / "section_spec.json"
TOC_PATH = REPO / "toc.json"

FENCE_RE = re.compile(r"^```(\w*)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def code_blocks(text: str) -> list[tuple[str, list[str]]]:
    """Return (language, lines) for every fenced block."""
    blocks: list[tuple[str, list[str]]] = []
    lang: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if m:
            if lang is None:
                lang = m.group(1) or "text"
                buf = []
            else:
                blocks.append((lang, buf))
                lang = None
        elif lang is not None:
            buf.append(line)
    return blocks


def strip_code(text: str) -> str:
    """Prose only — so that code cannot satisfy the prose requirements."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def section_body(text: str, heading: str) -> str:
    """Text under a `### heading` up to the next `###`."""
    marker = f"### {heading}"
    idx = text.find(marker)
    if idx < 0:
        return ""
    rest = text[idx + len(marker):]
    nxt = rest.find("\n### ")
    return rest if nxt < 0 else rest[:nxt]


def check_section(path: Path, spec: dict, rep: Report) -> None:
    where = str(path.relative_to(REPO))
    if not path.exists():
        rep.error(where, "listed in section_spec.json but missing on disk")
        return

    text = path.read_text(encoding="utf-8")
    prose = strip_code(text)
    thresholds = spec["thresholds"]

    headings = HEADING_RE.findall(text)
    for required in spec["required_headings"]:
        name = required.removeprefix("### ")
        # A trailing ": subtitle" is allowed, e.g. "### Code Detective: The XDC Conflict".
        if not any(h == name or h.startswith(name + ":") for h in headings):
            rep.error(where, f"missing required heading '### {name}'")

    blocks = code_blocks(text)
    if len(blocks) < thresholds["min_code_blocks"]:
        rep.error(
            where,
            f"{len(blocks)} code block(s); contract requires at least "
            f"{thresholds['min_code_blocks']}",
        )

    # The Real Artifact must actually be substantial and pasteable.
    artifact = section_body(text, "The Real Artifact")
    if artifact:
        art_blocks = code_blocks(artifact)
        if not art_blocks:
            rep.error(where, "'The Real Artifact' contains no code block")
        else:
            longest = max(len(b[1]) for b in art_blocks)
            if longest < thresholds["min_artifact_lines"]:
                rep.error(
                    where,
                    f"longest artifact block is {longest} lines; contract requires "
                    f"{thresholds['min_artifact_lines']}+ (a fragment is not an artifact)",
                )

    # Every question posed must be answered.
    answers = section_body(text, "Answers")
    if answers:
        for prompt in ("Brain Power", "Sharpen Your Pencil"):
            if prompt not in answers:
                rep.error(
                    where,
                    f"'### Answers' does not resolve '{prompt}' — "
                    "a section may not ask a question it never answers",
                )
        if len(answers.split()) < 150:
            rep.error(where, "'### Answers' is too thin to show any working")

    # Analogy table.
    mapping = section_body(text, "Analogy → Silicon")
    if mapping:
        rows = [ln for ln in mapping.splitlines() if TABLE_ROW_RE.match(ln)]
        # header + separator + at least two mappings
        if len(rows) < 4:
            rep.error(
                where,
                f"Analogy → Silicon table has {max(len(rows) - 2, 0)} mapping row(s); "
                "needs at least 2",
            )

    # Worked math must contain arithmetic, not just assertions.
    math = section_body(text, "Do the Math")
    if math and "=" not in math:
        rep.error(where, "'Do the Math' contains no equation")

    tables = sum(1 for ln in prose.splitlines() if TABLE_ROW_RE.match(ln))
    if tables < thresholds["min_tables"] * 4:
        rep.error(where, "no usable table found in prose")

    tool_hits = set(re.findall(spec["tool_token_pattern"], text))
    if len(tool_hits) < thresholds["min_tool_tokens"]:
        rep.error(
            where,
            f"only {len(tool_hits)} distinct tool/primitive name(s) "
            f"({', '.join(sorted(tool_hits)) or 'none'}); "
            f"contract requires {thresholds['min_tool_tokens']}",
        )

    units = re.findall(spec["units_pattern"], text)
    if len(units) < thresholds["min_numbers_with_units"]:
        rep.error(
            where,
            f"{len(units)} number(s) with units; contract requires "
            f"{thresholds['min_numbers_with_units']} — analogy without quantity is not engineering",
        )

    words = len(prose.split())
    if words < thresholds["min_words"]:
        rep.warn(where, f"{words} words of prose (target {thresholds['min_words']}+)")

    for banned in spec["banned_patterns"]:
        for m in re.finditer(banned["pattern"], prose):
            rep.warn(where, f"{m.group(0)!r} — {banned['reason']}")

    if "[REVIEW_STATUS:" not in text:
        rep.error(where, "missing REVIEW_STATUS trailer")


def check_toc(spec: dict, rep: Report) -> None:
    """The plan of record must match what is actually on disk."""
    toc = json.loads(TOC_PATH.read_text(encoding="utf-8"))
    where = "toc.json"
    spec_by_id = {s["id"]: s for s in spec["sections"]}
    seen: set[str] = set()

    for chapter in toc["chapters"]:
        for section in chapter["sections"]:
            sid = section["id"]
            seen.add(sid)
            target = REPO / "docs" / section["file"]
            if not target.exists():
                rep.error(
                    where,
                    f"section {sid} points at docs/{section['file']} which does not exist",
                )
                continue
            head = H1_RE.search(target.read_text(encoding="utf-8"))
            if head and section["title"].lower() not in head.group(1).lower():
                rep.error(
                    where,
                    f"section {sid} title {section['title']!r} does not appear in the "
                    f"file's H1 {head.group(1)!r}",
                )
            if sid not in spec_by_id:
                rep.error(where, f"section {sid} is not in authoring/section_spec.json")
            elif Path("docs") / section["file"] != Path(spec_by_id[sid]["file"]):
                rep.error(
                    where,
                    f"section {sid} file disagrees with section_spec.json "
                    f"(docs/{section['file']} vs {spec_by_id[sid]['file']})",
                )

    for sid in spec_by_id:
        if sid not in seen:
            rep.error(where, f"section {sid} is in the spec but missing from the TOC")


def check_nav(rep: Report) -> None:
    """mkdocs nav must not reference files that do not exist."""
    mkdocs = (REPO / "mkdocs.yml").read_text(encoding="utf-8")
    for ref in re.findall(r"(sections/[\w.]+\.md)", mkdocs):
        if not (REPO / "docs" / ref).exists():
            rep.error("mkdocs.yml", f"nav references docs/{ref} which does not exist")


def check_skills(spec: dict, rep: Report) -> None:
    """Agent skills must not drift out of sync with the book.

    The skills let an agent retrieve from the book without reading 74,000 words.
    That only works while the routing table knows about every section — a new
    section the index has never heard of is invisible to retrieval, which is the
    same class of silent drift that let toc.json point at eight files that did
    not exist.
    """
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.is_dir():
        return  # skills are optional; nothing to keep in sync

    for skill in ("fpga-ultrafast", "ultrafast-authoring"):
        path = skills_dir / skill / "SKILL.md"
        if not path.exists():
            rep.error(f".claude/skills/{skill}", "SKILL.md is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            rep.error(f".claude/skills/{skill}/SKILL.md", "missing YAML frontmatter")
            continue
        front = text.split("---", 2)[1]
        for field in ("name:", "description:"):
            if field not in front:
                rep.error(
                    f".claude/skills/{skill}/SKILL.md",
                    f"frontmatter has no '{field.rstrip(':')}' — skills trigger on it",
                )

    index = skills_dir / "fpga-ultrafast" / "references" / "topic-index.md"
    if not index.exists():
        rep.error(".claude/skills/fpga-ultrafast", "references/topic-index.md is missing")
        return

    index_text = index.read_text(encoding="utf-8")
    where = ".claude/skills/fpga-ultrafast/references/topic-index.md"
    for entry in spec["sections"]:
        sid = entry["id"]
        # Match the id as a standalone token so "1.1" does not match "11.1".
        if not re.search(rf"(?<![\d.]){re.escape(sid)}(?![\d.])", index_text):
            rep.error(
                where,
                f"section {sid} is not routed to from the topic index — "
                "agents will not find it",
            )


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    rep = Report()

    for entry in spec["sections"]:
        check_section(REPO / entry["file"], spec, rep)

    check_toc(spec, rep)
    check_nav(rep)
    check_skills(spec, rep)

    on_disk = {p.name for p in (REPO / "docs" / "sections").glob("*.md")}
    in_spec = {Path(s["file"]).name for s in spec["sections"]}
    for orphan in sorted(on_disk - in_spec):
        rep.error("docs/sections", f"{orphan} is not covered by the authoring spec")

    for w in rep.warnings:
        print(f"warning: {w}")
    for e in rep.errors:
        print(f"error:   {e}")

    print()
    print(
        f"{len(spec['sections'])} sections checked, "
        f"{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)"
    )
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
