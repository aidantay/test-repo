from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from shared_libs.io import read_fasta, setup_logging, write_csv, write_fasta
from shared_libs.models import Rec
from shared_libs.utils import is_standard_aa

if TYPE_CHECKING:
    import logging
    from collections.abc import Sequence


def windows(
    inputs: list[str | Path],
    out_faa: Path,
    out_csv: Path,
    min_len: int,
    max_len: int,
    step: int,
    allow_nonstd: bool = False,
    logger: logging.Logger | None = None,
) -> None:
    """Extract overlapping peptide windows from input proteome FASTA files.

    Generates sliding window peptide candidates of variable length across all input
    proteome sequences. Filters candidate windows containing ambiguous amino acid
    characters unless explicitly permitted.

    Args:
        inputs: Input proteome FASTA path(s).
        out_faa: Output FASTA path to extracted candidate windows.
        out_csv: Output CSV path to candidate catalog metadata.
        min_len: Minimum peptide window length in amino acids.
        max_len: Maximum peptide window length in amino acids.
        step: Stride size between window start positions.
        allow_nonstd: If True, allow ambiguous amino acid
            characters (X, B, Z, U) (default: False).
        logger: Logger for diagnostic messages (default: None).
    """
    if logger:
        logger.info(f"Extracting peptide windows from {len(inputs)} input file(s)...")
        logger.debug(
            f"Function parameters: "
            f"min_len={min_len}, "
            f"max_len={max_len}, "
            f"step={step}, "
            f"allow_nonstd={allow_nonstd}"
        )

    rows: list[dict[str, Any]] = []
    recs: list[Rec] = []

    for fasta_path in inputs:
        fasta_path = Path(fasta_path)
        src = fasta_path.name
        for protein in read_fasta(fasta_path, logger=logger):
            # Strip stop codon characters before windowing
            seq = protein.seq.replace("*", "")
            for length in range(min_len, max_len + 1):
                for start in range(0, len(seq) - length + 1, step):
                    pep = seq[start : start + length]
                    if not allow_nonstd and not is_standard_aa(pep):
                        continue
                    hid = (
                        f"pep|src={src}|prot={protein.id}"
                        f"|start={start + 1}|len={length}"
                    )
                    recs.append(Rec(hid, pep))
                    rows.append(
                        {
                            "id": hid,
                            "source_fasta": src,
                            "protein_id": protein.id,
                            "start_aa_1based": start + 1,
                            "length": length,
                            "peptide": pep,
                        }
                    )

    write_fasta(recs, out_faa, logger=logger)
    write_csv(rows, out_csv, logger=logger)
    if logger:
        logger.info("Summary:")
        logger.info(f"  - Extracted: {len(recs)} peptide window(s)")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Stage 1 - Extract overlapping peptide windows."
    )
    parser.add_argument(
        "--inputs",  "-i", type=Path, required=True, nargs="+",
        help="Input proteome FASTA file(s)"
    )
    parser.add_argument(
        "--out-faa", "-o", type=Path, required=True,
        help="Output FASTA file of extracted candidate peptides"
    )
    parser.add_argument(
        "--out-csv", "-c", type=Path, required=True,
        help="Output CSV file of peptide metadata"
    )
    parser.add_argument(
        "--min-len",       type=int,  required=True,
        help="Minimum peptide length"
    )
    parser.add_argument(
        "--max-len",       type=int,  required=True,
        help="Maximum peptide length"
    )
    parser.add_argument(
        "--step",          type=int,  required=True,
        help="Step size for sliding window"
    )
    parser.add_argument(
        "--allow-nonstd", action="store_true",
        help="Allow non-standard amino acids (default: False)"
    )
    parser.add_argument(
        "--log-file",      type=Path,
        help="Output log file"
    )
    args = parser.parse_args(argv)

    logger = None
    if args.log_file:
        logger = setup_logging(args.log_file, "01-windows")

    if logger:
        cmd_tokens = sys.argv if argv is None else ["01-windows", *argv]
        logger.debug(f"Command: {shlex.join(cmd_tokens)}")

    windows(
        inputs=args.inputs,
        out_faa=args.out_faa,
        out_csv=args.out_csv,
        min_len=args.min_len,
        max_len=args.max_len,
        step=args.step,
        allow_nonstd=args.allow_nonstd,
        logger=logger,
    )


if __name__ == "__main__":
    main()
