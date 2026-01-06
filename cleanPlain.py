
#!/usr/bin/env python3
"""
Delete bare 'qN.tex' files from 'questions' subfolders while keeping 'qN_xm.tex' and 'qN_soln.tex'.

Behavior:
- Walk immediate subfolders of the root (or recursively with --recursive).
- Ignore directories named: xmScripts, .vscode, .git
- In each found subfolder, if a 'questions' subfolder exists:
    * Delete files matching 'q<digits>.tex' (e.g., q1.tex, q23.tex)
    * Keep files like 'q<digits>_xm.tex' and 'q<digits>_soln.tex'
- Supports --dry-run to preview deletions.
- Supports --recursive to process nested subfolders.
- Supports --quiet to reduce output.

Usage examples:
  python delete_q_plain.py
  python delete_q_plain.py --dry-run
  python delete_q_plain.py --recursive
  python delete_q_plain.py --dry-run --recursive
"""

import argparse
import re
from pathlib import Path

IGNORE_DIRS = {"xmScripts", ".vscode", ".git"}

# Regex to match plain qN.tex (e.g., q1.tex, q23.tex) but not qN_xm.tex or qN_soln.tex
PLAIN_Q_REGEX = re.compile(r"^q(\d+)\.tex$")
PROTECTED_REGEX = re.compile(r"^q(\d+)_(xm|soln)\.tex$")

def find_candidate_deletions(questions_dir: Path) -> list[Path]:
    """
    Return a list of files in questions_dir that are plain 'qN.tex' and not protected variants.
    """
    candidates = []
    for p in questions_dir.glob("q*.tex"):
        name = p.name
        if PROTECTED_REGEX.match(name):
            # Keep files like qN_xm.tex, qN_soln.tex
            continue
        if PLAIN_Q_REGEX.match(name):
            candidates.append(p)
    return candidates

def gather_target_dirs(root: Path, recursive: bool) -> list[Path]:
    """
    Gather subdirectories to inspect (excluding IGNORE_DIRS).
    """
    if recursive:
        dirs = [d for d in root.rglob("*") if d.is_dir()]
    else:
        dirs = [d for d in root.iterdir() if d.is_dir()]

    return [d for d in dirs if d.name not in IGNORE_DIRS]

def main():
    parser = argparse.ArgumentParser(
        description="Delete 'qN.tex' from 'questions' folders, preserving 'qN_xm.tex' and 'qN_soln.tex'."
    )
    parser.add_argument("root", nargs="?", default=".", help="Root directory (default: current folder)")
    parser.add_argument("--dry-run", action="store_true", help="Preview deletions without removing files")
    parser.add_argument("--recursive", action="store_true", help="Process nested subfolders as well")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not args.quiet:
        print(f"[INFO] Root: {root}")
        if args.recursive:
            print("[INFO] Mode: recursive")
        if args.dry_run:
            print("[INFO] Dry-run: no files will be deleted")

    dirs = gather_target_dirs(root, args.recursive)
    total_deleted = 0
    total_candidates = 0

    for d in sorted(dirs):
        qdir = d / "questions"
        if not qdir.is_dir():
            continue

        candidates = find_candidate_deletions(qdir)
        total_candidates += len(candidates)

        if not candidates and not args.quiet:
            print(f"[SKIP] {qdir}: no plain qN.tex files found")
            continue

        for f in candidates:
            if args.dry_run:
                print(f"[DRY] Would delete: {f}")
            else:
                try:
                    f.unlink()
                    print(f"[DEL] Deleted: {f}")
                    total_deleted += 1
                except Exception as e:
                    print(f"[ERR] Could not delete {f}: {e}")

    if args.dry_run:
        print(f"[SUMMARY] {total_candidates} plain qN.tex file(s) would be deleted.")
    else:
        print(f"[SUMMARY] Deleted {total_deleted} plain qN.tex file(s).")

if __name__ == "__main__":
    main()
