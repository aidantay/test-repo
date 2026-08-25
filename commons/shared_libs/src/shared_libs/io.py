from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import polars as pl

from shared_libs.models import Rec

if TYPE_CHECKING:
    from collections.abc import Iterable


def read_fasta(path: str | Path, logger: logging.Logger | None = None) -> list[Rec]:
    """Parse a FASTA file and return a list of Rec objects.

    Sequences are upper-cased on read. Blank lines are ignored. The parser
    handles multi-line sequences correctly by accumulating chunks and joining
    at each record boundary, which is O(n) unlike repeated string concatenation.

    Args:
        path: Path to the FASTA file.
        logger: Logger to record diagnostic messages.

    Returns:
        List of Rec objects in file order.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    recs: list[Rec] = []
    current_id: str | None = None
    current_desc: str = ""
    chunks: list[str] = []

    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    recs.append(Rec(current_id, "".join(chunks).upper(), current_desc))
                head = line[1:]
                current_id = head.split()[0]
                current_desc = head
                chunks = []
            else:
                chunks.append(line)

    if current_id is not None:
        recs.append(Rec(current_id, "".join(chunks).upper(), current_desc))

    if logger:
        logger.info(f"Read {len(recs)} entries from {path}")
    return recs


def write_fasta(
    recs: Iterable[Rec],
    path: str | Path,
    width: int = 60,
    logger: logging.Logger | None = None,
) -> None:
    """Write records to a FASTA file, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as out:
        for r in recs:
            out.write(f">{r.id}\n")
            for i in range(0, len(r.seq), width):
                out.write(r.seq[i : i + width] + "\n")
    if logger:
        logger.info(f"Wrote FASTA records to {path}")


def write_csv(
    rows: list[dict[str, Any]],
    path: str | Path,
    fieldnames: list[str] | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """Write a list of dicts to a CSV, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        schema = dict.fromkeys(fieldnames or [], pl.String)
        df = pl.DataFrame(schema=schema)
    else:
        formatted_rows = [
            {k: str(v) if isinstance(v, bool) else v for k, v in r.items()}
            for r in rows
        ]
        df = pl.DataFrame(formatted_rows)
        if fieldnames:
            df = df.select(fieldnames)
    df.write_csv(path)
    if logger:
        logger.info(f"Wrote CSV rows to {path}")


def _count_fasta(path: Path) -> int:
    """Return the number of records in a FASTA file without loading sequences.

    Counts '>' header lines, which is much faster than reading full sequences
    for large files. Used to report candidate counts between pipeline stages.

    Args:
        path: Path to the FASTA file.

    Returns:
        Number of records, or 0 if the file does not exist.
    """
    if not path.exists():
        return 0
    count = 0
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                count += 1
    return count


def setup_logging(log_path: Path, name: str = "stage") -> logging.Logger:
    """Configure a stage logger that writes to a timestamped log file.

    The log captures run parameters, stage timings, candidate counts at
    each stage, warnings (Hamming violations, immunodominance), and any
    errors. This provides an audit trail for comparing runs across
    different parameter configurations.

    Args:
        log_path: Path to the log file. Parent directories are created
                  if they do not exist.
        name: Name of the stage logger (default: 'stage').

    Returns:
        Configured Logger instance.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            "%(asctime)s  %(levelname)-8s  [%(name)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(fh)

    return logger
