from __future__ import annotations

from shared_libs.constants import AA, BOVINE_RA, KD


def is_standard_aa(seq: str) -> bool:
    """Return True if all characters in seq are standard amino acids."""
    return all(c in AA for c in seq)


def kmers(seq: str, k: int) -> set[str]:
    """Return the set of all unique overlapping k-mers in seq."""
    if k <= 0 or len(seq) < k:
        return set()
    return {seq[i : i + k] for i in range(len(seq) - k + 1)}


def max_run(seq: str, chars: set[str]) -> int:
    """Return the length of the longest consecutive run of characters in chars."""
    if not seq:
        return 0
    max_len = 0
    current_len = 0
    for char in seq:
        if char in chars:
            current_len += 1
            if current_len > max_len:
                max_len = current_len
        else:
            current_len = 0
    return max_len
