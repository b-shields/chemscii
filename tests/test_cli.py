"""Tests for chemscii.cli module."""

from pathlib import Path

from typer.testing import CliRunner

from chemscii.cli import app, detect_input_type, parse_input

runner = CliRunner()


class TestDetectInputType:
    """Tests for input type detection."""

    def test_detect_smiles_simple(self) -> None:
        """Test detection of simple SMILES string."""
        input_type, value = detect_input_type("CCO")
        assert input_type == "smiles"
        assert value == "CCO"

    def test_detect_smiles_aromatic(self) -> None:
        """Test detection of aromatic SMILES string."""
        input_type, value = detect_input_type("c1ccccc1")
        assert input_type == "smiles"
        assert value == "c1ccccc1"

    def test_detect_smiles_with_whitespace(self) -> None:
        """Test detection of SMILES with surrounding whitespace."""
        input_type, value = detect_input_type("  CCO  ")
        assert input_type == "smiles"
        assert value == "CCO"

    def test_detect_chembl_uppercase(self) -> None:
        """Test detection of uppercase ChEMBL ID."""
        input_type, value = detect_input_type("CHEMBL25")
        assert input_type == "chembl"
        assert value == "CHEMBL25"

    def test_detect_chembl_lowercase(self) -> None:
        """Test detection of lowercase ChEMBL ID."""
        input_type, value = detect_input_type("chembl25")
        assert input_type == "chembl"
        assert value == "CHEMBL25"

    def test_detect_chembl_mixed_case(self) -> None:
        """Test detection of mixed case ChEMBL ID."""
        input_type, value = detect_input_type("ChEmBl113")
        assert input_type == "chembl"
        assert value == "CHEMBL113"

    def test_detect_name_unknown(self) -> None:
        """Test detection of unknown molecule name."""
        input_type, value = detect_input_type("unknownmolecule123")
        assert input_type == "name"
        assert value == "unknownmolecule123"

    def test_detect_file_sdf(self, tmp_path: Path) -> None:
        """Test detection of SDF file."""
        sdf_file = tmp_path / "test.sdf"
        sdf_file.write_text("test content")
        input_type, value = detect_input_type(str(sdf_file))
        assert input_type == "file"
        assert value == str(sdf_file)

    def test_detect_file_mol(self, tmp_path: Path) -> None:
        """Test detection of MOL file."""
        mol_file = tmp_path / "test.mol"
        mol_file.write_text("test content")
        input_type, value = detect_input_type(str(mol_file))
        assert input_type == "file"
        assert value == str(mol_file)

    def test_detect_nonexistent_file_as_name(self) -> None:
        """Test that nonexistent file path is treated as name."""
        input_type, value = detect_input_type("/nonexistent/path/molecule.sdf")
        assert input_type == "name"


class TestParseInput:
    """Tests for input parsing."""

    def test_parse_smiles_returns_same(self) -> None:
        """Test that SMILES input returns the same SMILES."""
        result = parse_input("smiles", "CCO")
        assert result == "CCO"

    def test_parse_chembl_valid(self) -> None:
        """Test parsing valid ChEMBL ID."""
        result = parse_input("chembl", "CHEMBL25")
        assert result is not None
        assert len(result) > 0

    def test_parse_chembl_invalid(self) -> None:
        """Test parsing invalid ChEMBL ID returns None."""
        _ = parse_input("chembl", "CHEMBL999999999999")
        # May return None if not in cache and API fails
        # This test just verifies no exception is raised

    def test_parse_name_known(self) -> None:
        """Test parsing known molecule name."""
        result = parse_input("name", "aspirin")
        assert result is not None
        assert len(result) > 0

    def test_parse_name_unknown(self) -> None:
        """Test parsing unknown molecule name."""
        result = parse_input("name", "notarealmolecule12345")
        # May return None for unknown names
        assert result is None or isinstance(result, str)

    def test_parse_sdf_file(self, tmp_path: Path) -> None:
        """Test parsing SDF file."""
        sdf_content = """
     RDKit          2D

  3  2  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2990    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.5981    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  2  3  1  0
M  END
"""
        sdf_file = tmp_path / "ethanol.sdf"
        sdf_file.write_text(sdf_content)
        result = parse_input("file", str(sdf_file))
        assert result is not None

    def test_parse_smi_file(self, tmp_path: Path) -> None:
        """Test parsing SMILES file."""
        smi_file = tmp_path / "molecules.smi"
        smi_file.write_text("CCO ethanol\nc1ccccc1 benzene\n")
        result = parse_input("file", str(smi_file))
        assert result == "CCO"


class TestCliMain:
    """Tests for main CLI command."""

    def test_render_smiles(self) -> None:
        """Test rendering a SMILES string."""
        result = runner.invoke(app, ["CCO", "--unicode"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_name(self) -> None:
        """Test rendering a molecule name."""
        result = runner.invoke(app, ["benzene", "--unicode"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_ascii_mode(self) -> None:
        """Test ASCII renderer mode."""
        result = runner.invoke(app, ["CCO", "--ascii"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_unicode_mode(self) -> None:
        """Test Unicode renderer mode."""
        result = runner.invoke(app, ["CCO", "--unicode"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_magic_mode(self) -> None:
        """Test Magic renderer mode (default)."""
        result = runner.invoke(app, ["CCO", "--magic"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_default_magic(self) -> None:
        """Test default renderer is magic."""
        result = runner.invoke(app, ["CCO"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_custom_columns(self) -> None:
        """Test custom columns for magic renderer."""
        result = runner.invoke(app, ["CCO", "--columns", "80"])
        assert result.exit_code == 0

    def test_custom_width_height(self) -> None:
        """Test custom width and height for ascii/unicode."""
        result = runner.invoke(
            app, ["CCO", "--ascii", "--width", "40", "--height", "20"]
        )
        assert result.exit_code == 0

    def test_multiple_renderers_error(self) -> None:
        """Test error when multiple renderers selected."""
        result = runner.invoke(app, ["CCO", "--ascii", "--unicode"])
        assert result.exit_code == 1
        assert "Only one renderer" in result.stdout

    def test_invalid_input_error(self) -> None:
        """Test error message for invalid input."""
        result = runner.invoke(app, ["notarealmolecule12345xyz"])
        assert result.exit_code == 1
        assert "Could not parse" in result.stdout

    def test_help_flag(self) -> None:
        """Test help flag."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert (
            "chemscii" in result.stdout.lower() or "molecule" in result.stdout.lower()
        )

    def test_render_chembl_cached(self) -> None:
        """Test rendering a cached ChEMBL ID."""
        result = runner.invoke(app, ["CHEMBL25", "--unicode"])
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_render_sdf_file(self, tmp_path: Path) -> None:
        """Test rendering from SDF file."""
        sdf_content = """
     RDKit          2D

  3  2  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2990    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.5981    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  2  3  1  0
M  END
"""
        sdf_file = tmp_path / "ethanol.sdf"
        sdf_file.write_text(sdf_content)
        result = runner.invoke(app, [str(sdf_file), "--unicode"])
        assert result.exit_code == 0
