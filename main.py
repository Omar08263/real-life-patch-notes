"""Write the competition's single patch-note line to /output/entry.txt.

The line is fixed text chosen for this competition; the program's job is to
emit it byte-for-byte, every run, with nothing read from the network, the
environment, or any file at run time.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

NOTE = (
    "v2.4.1: fixed a bug where the bladder's low-battery warning "
    "fired only after the last restroom had closed."
)
DESTINATION = Path("/output/entry.txt")
MAX_CHARS = 160


def validate(note: str) -> bytes:
    """Return the note as UTF-8 bytes, refusing anything outside the gate."""
    if not note.strip():
        raise ValueError("patch note is blank")
    if "\n" in note or "\r" in note:
        raise ValueError("patch note must be a single line")
    if len(note) > MAX_CHARS:
        raise ValueError(f"patch note is {len(note)} chars, over the {MAX_CHARS} cap")
    return note.encode("utf-8")


def write_entry(payload: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(payload)
    dest.chmod(0o644)
    reread = dest.read_bytes()
    if hashlib.sha256(reread).digest() != hashlib.sha256(payload).digest():
        raise RuntimeError("entry.txt on disk does not match the intended bytes")


def main() -> None:
    write_entry(validate(NOTE), DESTINATION)


if __name__ == "__main__":
    main()
