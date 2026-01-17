"""Tests for chemscii.mcp module."""

from __future__ import annotations

import pytest

from chemscii.mcp import _render, _resolve_smiles, render_molecule


class TestResolveSmiles:
    """Tests for SMILES resolution."""

    def test_resolve_smiles_direct(self) -> None:
        """Test resolving direct SMILES string."""
        result = _resolve_smiles("CCO")
        assert result == "CCO"

    def test_resolve_smiles_aromatic(self) -> None:
        """Test resolving aromatic SMILES."""
        result = _resolve_smiles("c1ccccc1")
        assert result == "c1ccccc1"

    def test_resolve_smiles_complex(self) -> None:
        """Test resolving complex SMILES."""
        result = _resolve_smiles("CC(=O)O")
        assert result == "CC(=O)O"

    def test_resolve_name_aspirin(self) -> None:
        """Test resolving molecule name."""
        result = _resolve_smiles("aspirin")
        assert result is not None
        assert len(result) > 0

    def test_resolve_name_benzene(self) -> None:
        """Test resolving benzene by name."""
        result = _resolve_smiles("benzene")
        assert result is not None
        assert "c" in result.lower() or "C" in result

    def test_resolve_chembl_id(self) -> None:
        """Test resolving ChEMBL ID."""
        result = _resolve_smiles("CHEMBL25")
        assert result is not None
        assert len(result) > 0

    def test_resolve_sdf_content(self) -> None:
        """Test resolving SDF content."""
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
        result = _resolve_smiles(sdf_content)
        assert result is not None
        # Should return SMILES for ethanol-like structure
        assert "C" in result or "c" in result

    def test_resolve_invalid_returns_none(self) -> None:
        """Test that invalid input returns None."""
        result = _resolve_smiles("notarealmolecule12345xyz")
        assert result is None


class TestRender:
    """Tests for rendering function."""

    def test_render_ascii(self) -> None:
        """Test ASCII renderer."""
        result = _render(
            "CCO", "ascii", width=40, height=20, columns=50, escape_codes=False
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_unicode(self) -> None:
        """Test Unicode renderer."""
        result = _render(
            "CCO", "unicode", width=40, height=20, columns=50, escape_codes=False
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_magic(self) -> None:
        """Test Magic renderer."""
        result = _render(
            "CCO", "magic", width=40, height=20, columns=50, escape_codes=False
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_invalid_smiles_raises(self) -> None:
        """Test that invalid SMILES raises ValueError."""
        with pytest.raises(ValueError, match="Failed to parse SMILES"):
            _render(
                "invalid_smiles_xyz",
                "ascii",
                width=40,
                height=20,
                columns=50,
                escape_codes=False,
            )

    def test_render_benzene_ascii(self) -> None:
        """Test rendering benzene with ASCII."""
        result = _render(
            "c1ccccc1", "ascii", width=40, height=20, columns=50, escape_codes=False
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_custom_dimensions(self) -> None:
        """Test rendering with custom dimensions."""
        result = _render(
            "CCO", "unicode", width=80, height=40, columns=100, escape_codes=False
        )
        assert isinstance(result, str)


class TestRenderMoleculeTool:
    """Tests for the MCP tool function."""

    def test_render_molecule_smiles(self) -> None:
        """Test rendering molecule from SMILES."""
        result = render_molecule("CCO")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_name(self) -> None:
        """Test rendering molecule from name."""
        result = render_molecule("ethanol")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_ascii_renderer(self) -> None:
        """Test rendering with ASCII renderer."""
        result = render_molecule("CCO", renderer="ascii")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_unicode_renderer(self) -> None:
        """Test rendering with Unicode renderer."""
        result = render_molecule("CCO", renderer="unicode")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_magic_renderer(self) -> None:
        """Test rendering with Magic renderer."""
        result = render_molecule("CCO", renderer="magic")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_custom_width_height(self) -> None:
        """Test rendering with custom width and height."""
        result = render_molecule("CCO", renderer="ascii", width=80, height=40)
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_custom_columns(self) -> None:
        """Test rendering with custom columns."""
        result = render_molecule("CCO", renderer="magic", columns=80)
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_invalid_input(self) -> None:
        """Test rendering with invalid input returns error message."""
        result = render_molecule("notarealmolecule12345xyz")
        assert isinstance(result, str)
        assert "Error" in result

    def test_render_molecule_chembl(self) -> None:
        """Test rendering ChEMBL ID."""
        result = render_molecule("CHEMBL25")
        assert isinstance(result, str)
        assert "Error" not in result

    def test_render_molecule_sdf_content(self) -> None:
        """Test rendering SDF content."""
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
        result = render_molecule(sdf_content)
        assert isinstance(result, str)
        assert "Error" not in result
