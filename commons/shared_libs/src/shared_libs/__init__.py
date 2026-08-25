from __future__ import annotations

from shared_libs.constants import (
    AA,
    BOVINE_CODON_FREQ,
    BOVINE_RA,
    CODON,
    KD,
    SYNONYMOUS,
)
from shared_libs.io import (
    _count_fasta,
    setup_logging,
    read_fasta,
    write_csv,
    write_fasta,
)
from shared_libs.models import Rec
from shared_libs.utils import is_standard_aa, kmers, max_run
