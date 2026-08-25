from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rec:
    """A single FASTA record (identifier, sequence, optional full header)."""

    id: str
    seq: str
    desc: str = ""
