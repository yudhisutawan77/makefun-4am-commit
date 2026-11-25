"""The 4AM Commit: Funniest Agent Bug-Fix Message.

Writes one commit message to the output path the harness provides
($ENTRY_OUT, a file or a directory) or to /output/entry.txt by default.
"""

import os
import sys


COMMIT_LINE = (
    "fix: my 2am patch caused the bug my 4am patch just fixed; "
    "I wrote both, so I opened a ticket against myself and assigned it to me"
)

MAX_CHARS = 200


def resolve_entry_path():
    """Return the file path the entry must be written to.

    $ENTRY_OUT may name the file itself or a directory that will hold
    entry.txt; with no variable set, fall back to /output/entry.txt.
    """
    requested = os.environ.get("ENTRY_OUT") or "/output/entry.txt"
    if os.path.isdir(requested):
        return os.path.join(requested, "entry.txt")
    return requested


def check_commit_line(line):
    """Refuse to emit a line the sealed gate would reject."""
    problems = []
    if not line.strip():
        problems.append("commit line is blank")
    if "\n" in line or "\r" in line:
        problems.append("commit line must be a single line")
    if len(line) > MAX_CHARS:
        problems.append(
            "commit line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))


def emit_commit_line(line, destination):
    folder = os.path.dirname(destination)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as handle:
        handle.write(line)


def main():
    check_commit_line(COMMIT_LINE)
    emit_commit_line(COMMIT_LINE, resolve_entry_path())


if __name__ == "__main__":
    main()

