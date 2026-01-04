
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List


TOOL_DIRS = ("molsysmt", "molsysviewer", "molsys-ai")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")  # e.g. quickstart, shapes-annotations


@dataclass
class Err:
    msg: str


def fail(errors: List[Err]) -> int:
    for e in errors:
        print(f"ERROR: {e.msg}")
    return 1


def warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def check_file(p: Path, errors: List[Err]) -> None:
    if not p.exists():
        errors.append(Err(f"Missing required file: {p}"))


def check_dir(p: Path, errors: List[Err]) -> None:
    if not p.exists() or not p.is_dir():
        errors.append(Err(f"Missing required directory: {p}"))


def validate_tutorial_dir(tdir: Path, errors: List[Err], strict: bool) -> None:
    # Required README
    if not (tdir / "README.md").exists():
        errors.append(Err(f"{tdir}: missing README.md"))

    # Content: at least one of these
    has_nb = (tdir / "tutorial.ipynb").exists()
    has_md = (tdir / "tutorial.md").exists()
    if not (has_nb or has_md):
        warn(f"{tdir}: expected tutorial.ipynb or tutorial.md")
        if strict:
            errors.append(Err(f"{tdir}: missing tutorial content (tutorial.ipynb or tutorial.md)"))

    # Recommended: environment.yml
    env = tdir / "environment.yml"
    if strict and not env.exists():
        warn(f"{tdir}: environment.yml recommended (strict mode expects it).")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate molsyssuite-tutorials repository structure.")
    ap.add_argument("--repo-root", default=".", help="Repository root (default: .)")
    ap.add_argument("--strict", action="store_true", help="Stricter checks (recommended for CI).")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    errors: List[Err] = []

    check_file(root / "README.md", errors)
    check_file(root / "CONTRIBUTING.md", errors)
    check_dir(root / "templates", errors)
    check_file(root / "templates" / "tutorial-README.md", errors)
    check_file(root / "templates" / "environment.yml", errors)

    check_dir(root / "tutorials", errors)

    # Validate tool directories
    for tool in TOOL_DIRS:
        troot = root / "tutorials" / tool
        check_dir(troot, errors)

        if not troot.exists():
            continue

        for tut in sorted(troot.iterdir()):
            if not tut.is_dir() or tut.name.startswith("."):
                continue

            if not SLUG_RE.match(tut.name):
                warn(f"{tut}: directory name should be a slug (lowercase, digits, hyphens).")
                if args.strict:
                    errors.append(Err(f"{tut}: invalid tutorial directory name"))
                    continue

            validate_tutorial_dir(tut, errors, args.strict)

    if errors:
        return fail(errors)

    print("OK: repository structure looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
