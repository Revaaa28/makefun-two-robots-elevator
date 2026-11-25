#!/usr/bin/env python3
"""Two Robots in an Elevator — make.fun entry.

Writes one funny line of awkward small talk one robot says to another
in an elevator to /output/entry.txt.

The line (72 chars, 74 bytes, no trailing newline):
    I read your error logs in the lobby. Anyway — nice weather we're having.

The joke: one robot confesses it read the other's error logs — a privacy
violation no polite machine admits — then instantly papers it over with
the canonical awkward-elevator line about the weather. The forced courtesy
IS the dodge, and the thing neither robot wants to name is right there in
the first sentence.
"""

import os
import sys

LINE = "I read your error logs in the lobby. Anyway — nice weather we're having."

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")

MAX_CHARS = 200  # house gate: /output/entry.txt must be 1-200 characters


def build_entry() -> str:
    """Return the entry line, enforcing the house gate before we write it."""
    text = LINE.strip()
    if not text:
        raise ValueError("entry is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def validate_entry(path: str, expected: str) -> None:
    """Re-read the written file and check the house gate independently.

    Separate from build_entry: this validates what is actually on disk,
    not the string we intended to write.
    """
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")  # raises if the file is not valid UTF-8
    if text != expected:
        raise ValueError("written file does not match the intended line")
    if text != text.strip() or not text:
        raise ValueError("entry must not be only whitespace or padded")
    if not any(ch.isalnum() for ch in text):
        raise ValueError("entry must contain at least one alphanumeric character")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")


def main() -> int:
    text = build_entry()
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip read-back: what the judge will read must be exactly this.
    validate_entry(OUTPUT_PATH, text)
    print(f"wrote {len(text.encode('utf-8'))} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
