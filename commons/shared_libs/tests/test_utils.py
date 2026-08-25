from __future__ import annotations

import pytest

import shared_libs as tt


class TestIsStandardAA:
    """Tests for the is_standard_aa() amino acid validation function."""

    @pytest.mark.parametrize(
        ("seq", "expected"),
        [
            pytest.param("ACDEFGHIKLMNPQRSTVWY", True,  id="all-standard-amino-acids"),
            pytest.param("",                     True,  id="empty-string-is-valid"   ),
            pytest.param("ACDEFX",               False, id="ambiguous-residue-fails" ),
            pytest.param("acdef",                False, id="lowercase-residue-fails" ),
            pytest.param("MKLLT*",               False, id="stop-codon-fails"        ),
            pytest.param("ABCDEF",               False, id="non-standard-char-fails" ),
        ],
    )
    def test_is_standard_aa(self, seq: str, expected: bool):
        """Verify is_standard_aa correctly validates standard vs non-standard sequences."""
        # Arrange & Act
        result = tt.is_standard_aa(seq)

        # Assert
        assert result is expected


class TestKmers:
    """Tests for the kmers() k-mer extraction function."""

    @pytest.mark.parametrize(
        ("seq", "k", "expected"),
        [
            pytest.param("ACDEF", 3, {"ACD", "CDE", "DEF"}, id="basic-kmer-extraction"   ),
            pytest.param("ACDEF", 5, {"ACDEF"},             id="k-equals-sequence-length"),
            pytest.param("ABC",   5, set(),                 id="k-longer-than-sequence"  ),
            pytest.param("",      3, set(),                 id="empty-sequence"          ),
            pytest.param("AAAA",  2, {"AA"},                id="duplicates-collapsed"    ),
        ],
    )
    def test_kmers(self, seq: str, k: int, expected: set[str]):
        """Verify kmers extracts unique k-mers of specified length."""
        # Arrange & Act
        result = tt.kmers(seq, k)

        # Assert
        assert result == expected


class TestMaxRun:
    """Tests for the max_run() consecutive-character run detector."""

    @pytest.mark.parametrize(
        ("seq", "chars", "expected"),
        [
            pytest.param(
                "AAGGGGAA",
                {"G"},
                4,
                id="single-run",
            ),
            pytest.param(
                "GGGAAGGGGGG",
                {"G"},
                6,
                id="multiple-runs",
            ),
            pytest.param(
                "AAAA",
                {"G"},
                0,
                id="no-matching-chars",
            ),
            pytest.param(
                "UUUU",
                {"U"},
                4,
                id="entire-sequence-matches",
            ),
            pytest.param(
                "AIVLA",
                {"I", "V", "L", "F", "C", "M", "A", "W", "Y"},
                5,
                id="multiple-char-set",
            ),
            pytest.param("", {"G"}, 0, id="empty-sequence"),
        ],
    )
    def test_max_run(self, seq: str, chars: set[str], expected: int):
        """Verify max_run correctly counts consecutive runs of matching characters."""
        # Arrange & Act
        result = tt.max_run(seq, chars)

        # Assert
        assert result == expected
