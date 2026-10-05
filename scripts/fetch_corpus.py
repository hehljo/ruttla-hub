#!/usr/bin/env python3
"""Holt den Gesund-Korpus aus corpus.toml, je Repo genau den gepinnten Commit.

Gibt die Verzeichnisse als `--corpus DIR`-Argumente aus (eine Zeile), damit der
Aufrufer sie an `ruttla hub check` weiterreicht. Bricht ab, wenn ein Commit
nicht exakt so ankommt — ein falscher Korpus ist kein Korpus.
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path


def main() -> int:
    config, dest = Path(sys.argv[1]), Path(sys.argv[2])
    repos = tomllib.loads(config.read_text(encoding="utf-8")).get("repo", [])
    if not repos:
        print("corpus.toml: kein Repo — Falsch-Positiv-Lauf wäre nicht gemessen", file=sys.stderr)
        return 1
    args = []
    for repo in repos:
        url, commit = repo["url"], repo["commit"]
        target = dest / url.rstrip("/").rsplit("/", 1)[-1]
        if not target.is_dir():
            subprocess.run(["git", "init", "-q", str(target)], check=True)
            subprocess.run(["git", "-C", str(target), "fetch", "-q", "--depth", "1", url, commit], check=True)
            subprocess.run(["git", "-C", str(target), "checkout", "-q", "FETCH_HEAD"], check=True)
        head = subprocess.run(["git", "-C", str(target), "rev-parse", "HEAD"], check=True,
                              capture_output=True, text=True).stdout.strip()
        if head != commit:
            print(f"{url}: HEAD {head} ≠ gepinnt {commit}", file=sys.stderr)
            return 1
        args += ["--corpus", str(target)]
    print(" ".join(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
