from __future__ import annotations

import pytest
from shared_libs.io import read_fasta, write_fasta
from shared_libs.models import Rec

from windows.main import main, windows


@pytest.fixture
def make_fasta(tmp_path):
    """Stage-local fixture factory for generating input FASTA files."""

    def _make_fasta(
        filename: str = "proteome.faa",
        records: list[tuple[str, str] | Rec] | None = None,
    ):
        path = tmp_path / filename
        records = records if records else []
        formatted = [r if isinstance(r, Rec) else Rec(r[0], r[1]) for r in records]
        write_fasta(formatted, path)
        return path

    return _make_fasta


@pytest.fixture
def out_faa(tmp_path):
    """Fixture providing standard output FASTA path."""
    return tmp_path / "peptides.faa"


@pytest.fixture
def out_csv(tmp_path):
    """Fixture providing standard output CSV path."""
    return tmp_path / "peptides.csv"


@pytest.fixture
def log_file(tmp_path):
    """Fixture providing standard log file path."""
    return tmp_path / "stage.log"


SINGLE_PROTEIN_CASES = [
    pytest.param("std_len",     "ACDEFGHIKLMNP",     12, 12, 1, 2, id="standard-length-13aa"    ),
    pytest.param("short_len",   "ACDEF",             12, 12, 1, 0, id="short-length-below-min"  ),
    pytest.param("exact_len",   "ACDEFGHIKLMN",      12, 12, 1, 1, id="exact-length-equal-min"  ),
    pytest.param("stepped_len", "ACDEFGHIKLMNPQRST", 12, 12, 2, 3, id="stepped-length-step2"    ),
    pytest.param("non_std_aa",  "MKLX*VTACDEFGH",    12, 12, 1, 0, id="non-standard-aa-filtered"),
]


class TestWindows:
    """Tests for the Windows stage programmatic interface."""

    @pytest.mark.parametrize(
        ("seq_id", "sequence", "min_len", "max_len", "step", "expected_count"),
        SINGLE_PROTEIN_CASES,
    )
    def test_programmatic_windows(
        self,
        make_fasta,
        out_faa,
        out_csv,
        seq_id,
        sequence,
        min_len,
        max_len,
        step,
        expected_count,
    ):
        """Test windows() programmatic execution on individual single-protein FASTA files."""
        # Arrange
        input_faa = make_fasta(records=[(seq_id, sequence)])

        # Act
        windows(
            [input_faa], out_faa, out_csv, min_len=min_len, max_len=max_len, step=step
        )

        # Assert
        recs = read_fasta(out_faa)
        assert len(recs) == expected_count


class TestWindowsCLI:
    """Tests for the Windows stage CLI interface."""

    @pytest.mark.parametrize(
        ("seq_id", "sequence", "min_len", "max_len", "step", "expected_count"),
        SINGLE_PROTEIN_CASES,
    )
    def test_cli_windows(
        self,
        make_fasta,
        out_faa,
        out_csv,
        seq_id,
        sequence,
        min_len,
        max_len,
        step,
        expected_count,
    ):
        """Test windows stage main() CLI entrypoint on individual single-protein FASTA files."""
        # Arrange
        input_faa = make_fasta(records=[(seq_id, sequence)])

        # Act
        main(
            [
                "-i",        str(input_faa),
                "-o",        str(out_faa),
                "-c",        str(out_csv),
                "--min-len", str(min_len),
                "--max-len", str(max_len),
                "--step",    str(step),
            ]
        )

        # Assert
        recs = read_fasta(out_faa)
        assert len(recs) == expected_count

    def test_cli_with_logging(self, make_fasta, out_faa, out_csv, log_file):
        """Test CLI interface with --log-file."""
        # Arrange
        input_faa = make_fasta(records=[("seq1", "ACDEFGHIKLMNP")])

        # Act
        main(
            [
                "-i",         str(input_faa),
                "-o",         str(out_faa),
                "-c",         str(out_csv),
                "--min-len",  "12",
                "--max-len",  "12",
                "--step",     "1",
                "--log-file", str(log_file),
            ]
        )

        # Assert
        assert out_faa.exists()
        assert log_file.exists()
