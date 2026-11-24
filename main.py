#!/usr/bin/env python3
"""One-Liner Laugh Lab entry.

Writes a single deadpan excuse from a robot vacuum to /output/entry.txt.
The line is exactly 96 characters: it must stay byte-identical, with no
trailing newline, so the gate (1-200 UTF-8 chars, not only whitespace) passes.
"""

import os

ENTRY_TEXT = "The sock entered my dustbin without a permit and is now in protective custody. I regret nothing."

OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> str:
    """Enforce the sealed-scorer gate for the entry line.

    UTF-8 text, 1-200 characters, not only whitespace, and exactly the
    intended 96-character line. Kept apart from main() so a bad line can
    never reach /output, and so the gate is unit-testable without writing
    a file. Returns the text unchanged.
    """
    text.encode("utf-8")
    assert 1 <= len(text) <= 200, "entry must be 1-200 characters"
    assert text.strip(), "entry must not be only whitespace"
    assert len(text) == 96, "entry must be exactly the 96-character line"
    return text


def main() -> None:
    text = validate(ENTRY_TEXT)
    encoded = text.encode("utf-8")

    os.makedirs("/output", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(encoded)
    # Best-effort readability on the file only. Never chmod /output itself:
    # the grader runs as a different uid and chmod on the directory fails
    # with EPERM.
    try:
        os.chmod(OUTPUT_PATH, 0o644)
    except OSError:
        pass


if __name__ == "__main__":
    main()
