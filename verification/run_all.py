"""Check navigation, learning-map integrity and the stored finite experiment.

Run from any directory with Python 3.12 or later. The default run needs the
pinned numerical dependencies. --structure-only uses only the standard library.
These checks do not prove the analytical claims or verify hosted rendering.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "llms.txt", "LICENSE", "learning/README.md",
    "learning/BRIDGE.md", "learning/MILESTONES.md", "science/model.md",
    "science/local_response.md", "science/reconstruction.md",
    "science/resources.md", "science/interpretation.md",
    "references/RELATED_WORK.md", "references/references.bib",
    "verification/README.md", "verification/verify_protocol.py",
    "verification/expected/protocol.json", "verification/requirements.txt",
)
FIELDS = (
    "Central question", "Understanding target", "Dependencies and story role",
    "Conceptual connection", "Sources",
)
ABS_TOL = 2e-9
REL_TOL = 2e-6


def prose(text: str) -> str:
    """Exclude fenced code, while detecting an unclosed fence."""
    out: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            out.append(line)
    if fence is not None:
        raise ValueError("Unclosed Markdown code fence")
    return "\n".join(out)


def anchors(text: str) -> set[str]:
    """Recognize explicit IDs and the simple GitHub headings used here."""
    text = prose(text)
    found = set(re.findall(r'<a\s+id=[\"\']([^\"\']+)[\"\']', text))
    counts: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        base = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        suffix = counts.get(base, 0)
        found.add(base if suffix == 0 else f"{base}-{suffix}")
        counts[base] = suffix + 1
    return found


def check_links(root: Path) -> tuple[int, int]:
    documents = sorted(root.rglob("*.md"))
    documents = [p for p in documents if not any(
        part in {".git", ".venv", "generated"} for part in p.relative_to(root).parts
    )]
    checked = 0
    for document in documents:
        raw = document.read_text(encoding="utf-8")
        text = prose(raw)
        if text.count("$`") != text.count("`$"):
            raise ValueError(f"{document}: unmatched inline math delimiter")
        definitions = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)", text, re.M))
        targets = re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", text)
        for label in re.findall(r"\[[^\]\n]+\]\[([^\]\n]+)\]", text):
            if label not in definitions:
                raise ValueError(f"{document}: undefined reference [{label}]")
            targets.append(definitions[label])
        for target in targets:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue  # External reachability is not an offline check.
            destination = (document.parent / unquote(parsed.path)).resolve()
            if not parsed.path:
                destination = document.resolve()
            if not destination.is_relative_to(root.resolve()):
                raise ValueError(f"{document}: link escapes repository: {target}")
            if not destination.exists():
                raise ValueError(f"{document}: missing link target: {target}")
            if parsed.fragment and destination.suffix == ".md":
                if unquote(parsed.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                    raise ValueError(f"{document}: missing anchor: {target}")
            checked += 1
    return len(documents), checked


def check_milestones(text: str) -> None:
    matches = list(re.finditer(r"^### M(\d{2}): .+$", text, re.M))
    if [int(m.group(1)) for m in matches] != list(range(1, 31)):
        raise ValueError("Expected exactly M01 through M30, in order")
    for index, match in enumerate(matches):
        number = index + 1
        end = matches[index + 1].start() if index < 29 else len(text)
        block = text[match.end():end]
        for field in FIELDS:
            if not re.search(rf"\*\*{re.escape(field)}:\*\*\s*\S", block):
                raise ValueError(f"M{number:02}: missing {field}")
        deps = re.search(r"\*\*Dependencies and story role:\*\*(.+)", block)
        assert deps is not None
        if any(int(dep) >= number for dep in re.findall(r"\bM(\d{2})\b", deps.group(1))):
            raise ValueError(f"M{number:02}: dependency is not an earlier milestone")
    if not set(f"m{i:02}" for i in range(1, 31)).issubset(anchors(text)):
        raise ValueError("Missing stable milestone anchors")
    background = text.find("## Background/preliminaries: M01–M11")
    narrative = text.find("## Narrative/innovation: M12–M30")
    if not (0 <= background < matches[0].start()
            < matches[10].start() < narrative < matches[11].start()):
        raise ValueError("The settled 11/19 phase allocation is inconsistent")
    if "Nielsen and Chuang" not in text or "10th Anniversary Edition (2010)" not in text:
        raise ValueError("The selected educational anchor is missing")


def compare(expected: Any, actual: Any, path: str = "$") -> None:
    """Compare every result field except top-level environment and wall time."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise ValueError(f"{path}: expected an object")
        ignored = {"environment", "runtime_seconds"} if path == "$" else set()
        keys = set(expected) - ignored
        if keys != set(actual) - ignored:
            raise ValueError(f"{path}: result keys differ")
        for key in sorted(keys):
            compare(expected[key], actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise ValueError(f"{path}: result list length/type differs")
        for index, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, f"{path}[{index}]")
    elif isinstance(expected, float):
        if (isinstance(actual, bool) or not isinstance(actual, (int, float))
                or not math.isfinite(expected) or not math.isfinite(actual)
                or not math.isclose(expected, actual, abs_tol=ABS_TOL, rel_tol=REL_TOL)):
            raise ValueError(f"{path}: {actual!r} differs from {expected!r}")
    elif type(expected) is not type(actual) or expected != actual:
        raise ValueError(f"{path}: {actual!r} differs from {expected!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--structure-only", action="store_true")
    args = parser.parse_args()
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing required file: {name}")
    documents, links = check_links(ROOT)
    check_milestones((ROOT / "learning/MILESTONES.md").read_text(encoding="utf-8"))
    print(f"PASS: {documents} Markdown files, {links} local links; 30 milestones (11/19).", flush=True)
    if args.structure_only:
        print("Numerical reproduction not requested; hosted rendering is not checked.")
        return 0

    generated = ROOT / "verification/generated"
    generated.mkdir(exist_ok=True)
    result_path = generated / "protocol.json"
    result_path.unlink(missing_ok=True)  # Never mistake a stale output for a rerun.
    completed = subprocess.run(
        [sys.executable, str(ROOT / "verification/verify_protocol.py"), "--output", str(result_path)],
        cwd=ROOT, capture_output=True, text=True, timeout=300, check=False,
    )
    (generated / "protocol.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (generated / "protocol.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode:
        raise ValueError(f"Numerical reproduction failed:\n{completed.stderr[-4000:]}")
    expected = json.loads((ROOT / "verification/expected/protocol.json").read_text(encoding="utf-8"))
    actual = json.loads(result_path.read_text(encoding="utf-8"))
    compare(expected, actual)
    print(f"PASS: stored results reproduced (absolute tolerance {ABS_TOL:g}, relative tolerance {REL_TOL:g}).")
    print("Recorded environment:", json.dumps(expected["environment"], sort_keys=True))
    print("Current environment:", json.dumps(actual["environment"], sort_keys=True))
    summary = actual["finite_shot_repetition_summary"]
    finite = actual["finite_shot_example"]
    print(f"Fixed-seed stage-bound successes: {summary['all_stage_bound_successes']}/{summary['count']}.")
    print(f"Represented shots per run: {finite['total_fresh_preparations']:,}; unknown-prefix calls: {finite['total_unknown_prefix_queries']:,}.")
    print("These are regression checks, not independent proof or hardware validation.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
