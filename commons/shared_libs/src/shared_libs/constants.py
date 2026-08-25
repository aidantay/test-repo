from __future__ import annotations

# The 20 standard amino acids in single-letter code.
AA: set[str] = set("ACDEFGHIKLMNPQRSTVWY")

# Kyte-Doolittle hydrophobicity scale (J. Mol. Biol. 157:105-132, 1982).
# Positive = hydrophobic, negative = hydrophilic.
KD: dict[str, float] = {
    "I": 4.5,
    "V": 4.2,
    "L": 3.8,
    "F": 2.8,
    "C": 2.5,
    "M": 1.9,
    "A": 1.8,
    "G": -0.4,
    "T": -0.7,
    "S": -0.8,
    "W": -0.9,
    "Y": -1.3,
    "P": -1.6,
    "H": -3.2,
    "E": -3.5,
    "Q": -3.5,
    "D": -3.5,
    "N": -3.5,
    "K": -3.9,
    "R": -4.5,
}

# All synonymous codons per amino acid.
_SYNONYMOUS_RAW: dict[str, list[str]] = {
    "A": ["GCT", "GCC", "GCA", "GCG"],
    "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "N": ["AAT", "AAC"],
    "D": ["GAT", "GAC"],
    "C": ["TGT", "TGC"],
    "Q": ["CAA", "CAG"],
    "E": ["GAA", "GAG"],
    "G": ["GGT", "GGC", "GGA", "GGG"],
    "H": ["CAT", "CAC"],
    "I": ["ATT", "ATC", "ATA"],
    "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "K": ["AAA", "AAG"],
    "M": ["ATG"],
    "F": ["TTT", "TTC"],
    "P": ["CCT", "CCC", "CCA", "CCG"],
    "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "T": ["ACT", "ACC", "ACA", "ACG"],
    "W": ["TGG"],
    "Y": ["TAT", "TAC"],
    "V": ["GTT", "GTC", "GTA", "GTG"],
    "*": ["TAA", "TAG", "TGA"],
}

# Bos taurus codon usage frequencies (relative within each synonymous family).
BOVINE_CODON_FREQ: dict[str, float] = {
    # Phe (F)
    "TTT": 0.44,
    "TTC": 0.56,
    # Leu (L)
    "TTA": 0.07,
    "TTG": 0.13,
    "CTT": 0.14,
    "CTC": 0.20,
    "CTA": 0.07,
    "CTG": 0.39,
    # Ile (I)
    "ATT": 0.35,
    "ATC": 0.47,
    "ATA": 0.18,
    # Met (M)
    "ATG": 1.00,
    # Val (V)
    "GTT": 0.18,
    "GTC": 0.23,
    "GTA": 0.12,
    "GTG": 0.47,
    # Ser (S)
    "TCT": 0.15,
    "TCC": 0.22,
    "TCA": 0.14,
    "TCG": 0.06,
    "AGT": 0.15,
    "AGC": 0.28,
    # Pro (P)
    "CCT": 0.27,
    "CCC": 0.33,
    "CCA": 0.27,
    "CCG": 0.13,
    # Thr (T)
    "ACT": 0.25,
    "ACC": 0.36,
    "ACA": 0.27,
    "ACG": 0.12,
    # Ala (A)
    "GCT": 0.25,
    "GCC": 0.41,
    "GCA": 0.23,
    "GCG": 0.11,
    # Tyr (Y)
    "TAT": 0.44,
    "TAC": 0.56,
    # Stop (*)
    "TAA": 0.28,
    "TAG": 0.20,
    "TGA": 0.52,
    # His (H)
    "CAT": 0.42,
    "CAC": 0.58,
    # Gln (Q)
    "CAA": 0.27,
    "CAG": 0.73,
    # Asn (N)
    "AAT": 0.46,
    "AAC": 0.54,
    # Lys (K)
    "AAA": 0.42,
    "AAG": 0.58,
    # Asp (D)
    "GAT": 0.46,
    "GAC": 0.54,
    # Glu (E)
    "GAA": 0.42,
    "GAG": 0.58,
    # Cys (C)
    "TGT": 0.46,
    "TGC": 0.54,
    # Trp (W)
    "TGG": 1.00,
    # Arg (R)
    "CGT": 0.08,
    "CGC": 0.19,
    "CGA": 0.10,
    "CGG": 0.21,
    "AGA": 0.21,
    "AGG": 0.21,
    # Gly (G)
    "GGT": 0.16,
    "GGC": 0.35,
    "GGA": 0.24,
    "GGG": 0.25,
}

# Preferred codon per amino acid.
CODON: dict[str, str] = {
    aa: max(codons, key=lambda c: BOVINE_CODON_FREQ.get(c, 0.0))
    for aa, codons in _SYNONYMOUS_RAW.items()
}

# Synonymous codons per amino acid, sorted by decreasing bovine frequency.
SYNONYMOUS: dict[str, list[str]] = {
    aa: sorted(codons, key=lambda c: BOVINE_CODON_FREQ.get(c, 0.0), reverse=True)
    for aa, codons in _SYNONYMOUS_RAW.items()
}

# Relative adaptiveness (Ra) for each codon.
BOVINE_RA: dict[str, float] = {}
for _aa, _codons in _SYNONYMOUS_RAW.items():
    _max_freq = max(BOVINE_CODON_FREQ.get(c, 0.0) for c in _codons)
    for _codon in _codons:
        BOVINE_RA[_codon] = (
            BOVINE_CODON_FREQ.get(_codon, 0.0) / _max_freq if _max_freq > 0 else 0.0
        )
