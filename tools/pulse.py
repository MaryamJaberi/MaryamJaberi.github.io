#!/usr/bin/env python3
"""Writes assets/pulse.json: how much each product changed, week by week.

Run from the repo root:  python3 tools/pulse.py [SRC_DIR]
SRC_DIR holds clones of the project repos (default: _src). Missing clones are skipped,
and the previous numbers for that product are kept.
The file has no timestamp of its own, so it only changes when the history changes.
"""
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_src"
START = date(2026, 10, 26)  # Monday of the week the portfolio's history begins
BOTS = {"github-actions[bot]", "github-actions"}

# product key -> list of (repo directory or None for this site, path filter or None)
SOURCES = {
    "tw": [(None, "wellbeing-check")],
    "planet": [("earth-through-time-new", None)],
    "tik": [("Dour-new", None)],
    "poly": [("Language-Learning-Party-Game-new", None)],
    "bazaar": [(None, "daneshsara"), (None, "psychology-wiki")],
    "night": [("Mafia-new", None)],
    "verse": [("ganjoor-no-new", None)],
}


def commits(repo: Path, path):
    cmd = ["git", "-C", str(repo), "log", "--no-merges", "--format=%aI%x09%an", f"--since={START.isoformat()}"]
    if path:
        cmd += ["--", path]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        return None
    rows = []
    for line in out.stdout.splitlines():
        when, _, who = line.partition("\t")
        if who in BOTS:
            continue
        rows.append(datetime.fromisoformat(when))
    return rows


def main():
    target = ROOT / "assets/pulse.json"
    old = json.loads(target.read_text()) if target.exists() else {"rows": {}}
    rows = {}
    for key, sources in SOURCES.items():
        stamps, ok = [], True
        for repo, path in sources:
            d = ROOT if repo is None else SRC / repo
            found = commits(d, path) if (d / ".git").exists() else None
            if found is None:
                ok = False
                break
            stamps += found
        if not ok:
            if key in old.get("rows", {}):
                rows[key] = old["rows"][key]
            continue
        weeks = {}
        for t in stamps:
            w = (t.date() - START).days // 7
            if w >= 0:
                weeks[str(w)] = weeks.get(str(w), 0) + 1
        last = max(stamps).isoformat(timespec="minutes") if stamps else None
        rows[key] = {"w": dict(sorted(weeks.items(), key=lambda kv: int(kv[0]))), "n": len(stamps), "last": last}
    data = {"start": START.isoformat(), "rows": rows}
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    if not target.exists() or target.read_text() != text:
        target.write_text(text)
        print("pulse.json updated")
    else:
        print("pulse.json unchanged")


if __name__ == "__main__":
    main()
