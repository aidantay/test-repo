from __future__ import annotations

import pytest

from shared_libs.io import _count_fasta, read_fasta, write_fasta
from shared_libs.models import Rec


@pytest.fixture
def make_fasta(tmp_path):
    """Local fixture factory for generating input FASTA files."""

    def _make_fasta(
        filename: str = "test.faa",
        records: list[tuple[str, str] | Rec] | None = None,
        width: int = 80,
    ):
        path = tmp_path / filename
        records = records if records else []
        formatted = [r if isinstance(r, Rec) else Rec(r[0], r[1]) for r in records]
        write_fasta(formatted, path, width=width)
        return path

    return _make_fasta


class TestFASTAIO:
    """Tests for FASTA file reading, writing, and counting functions."""

    def test_roundtrip_single_record(self, make_fasta):
        """Writing then reading a single record should recover the original."""
        # Arrange
        original = [Rec("seq1", "ACDEFGHIK", "seq1 test protein")]
        path = make_fasta(records=original)

        # Act
        recovered = read_fasta(path)

        # Assert
        assert len(recovered) == 1
        assert recovered[0].id == "seq1"
        assert recovered[0].seq == "ACDEFGHIK"

    def test_roundtrip_multiple_records(self, make_fasta):
        """Multiple records should all be recovered in order."""
        # Arrange
        original = [
            Rec("prot_A", "MKKLLT"),
            Rec("prot_B", "GGGSGGG"),
            Rec("prot_C", "TVLSGALA"),
        ]
        path = make_fasta(records=original)

        # Act
        recovered = read_fasta(path)

        # Assert
        assert len(recovered) == 3
        assert [r.id for r in recovered] == ["prot_A", "prot_B", "prot_C"]
        assert [r.seq for r in recovered] == ["MKKLLT", "GGGSGGG", "TVLSGALA"]

    def test_uppercase_on_read(self, make_fasta):
        """Sequences should be upper-cased regardless of how they are stored."""
        # Arrange
        path = make_fasta(records=[Rec("test", "acdefghik")])

        # Act
        records = read_fasta(path)

        # Assert
        assert records[0].seq == "ACDEFGHIK"

    def test_multiline_sequence(self, make_fasta):
        """Multi-line sequences should be joined correctly."""
        # Arrange
        path = make_fasta(records=[Rec("seq1", "ACDEFGHIKLMNPQR")])

        # Act
        records = read_fasta(path)

        # Assert
        assert records[0].seq == "ACDEFGHIKLMNPQR"

    def test_blank_lines_ignored(self, make_fasta):
        """Blank lines between sequence lines should not corrupt the record."""
        # Arrange
        path = make_fasta(records=[Rec("seq1", "ACDEFGHIKL")])

        # Act
        records = read_fasta(path)

        # Assert
        assert records[0].seq == "ACDEFGHIKL"

    def test_missing_file_raises(self, tmp_path):
        """Reading a non-existent file should raise FileNotFoundError."""
        # Arrange
        out_faa = tmp_path / "out.faa"

        # Act & Assert
        with pytest.raises(FileNotFoundError, match=r"out\.faa"):
            read_fasta(out_faa)

    def test_line_wrapping(self, tmp_path, make_fasta):
        """Written sequences should be wrapped at the specified width."""
        # Arrange
        out_faa = tmp_path / "out.faa"

        # Act
        write_fasta([Rec("s", "A" * 130)], out_faa, width=60)

        # Assert
        lines = out_faa.read_text().splitlines()
        assert lines[0] == ">s"
        assert len(lines[1]) == 60
        assert len(lines[2]) == 60
        assert len(lines[3]) == 10

    def test_correct_count(self, make_fasta):
        """Should count the correct number of records."""
        # Arrange
        path = make_fasta(
            records=[Rec("a", "AA"), Rec("b", "BB"), Rec("c", "CC")],
        )

        # Act & Assert
        assert _count_fasta(path) == 3

    def test_missing_file_returns_zero(self, tmp_path):
        """Missing file should return 0 rather than raising."""
        # Arrange
        out_faa = tmp_path / "out.faa"

        # Act & Assert
        assert _count_fasta(out_faa) == 0

    def test_write_fasta_logging(self, tmp_path):
        """write_fasta should log record counts when logger is provided."""
        import logging
        out_faa = tmp_path / "out.faa"
        logger = logging.getLogger("test_write_fasta")
        logs = []
        logger.info = lambda msg: logs.append(msg)

        write_fasta([Rec("r1", "ACGT"), Rec("r2", "TGCA")], out_faa, logger=logger)
        assert len(logs) == 1
        assert "Wrote FASTA records to" in logs[0]

    def test_write_csv_logging(self, tmp_path):
        """write_csv should log row counts when logger is provided."""
        import logging
        from shared_libs.io import write_csv

        out_csv = tmp_path / "out.csv"
        logger = logging.getLogger("test_write_csv")
        logs = []
        logger.info = lambda msg: logs.append(msg)

        write_csv([{"a": 1}, {"a": 2}], out_csv, logger=logger)
        assert len(logs) == 1
        assert "Wrote CSV rows to" in logs[0]
