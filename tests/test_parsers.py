"""Tests for chemscii.parsers module."""

from pathlib import Path

import pytest
from rdkit.Chem import Mol

from chemscii.parsers.molecule import parse_sdf, parse_smiles
from tests.fixtures.molecules import (
    BENZENE,
    CYCLOHEXANE,
    ETHANOL,
    ETHENE,
    ETHYNE,
    METHANE,
    SMILES_TEST_CASES,
    WATER,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestParseSmiles:
    """Tests for SMILES parsing."""

    def test_parse_simple_molecule(self) -> None:
        """Test parsing a simple SMILES string."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        assert isinstance(mol, Mol)

    def test_parse_returns_none_for_invalid_smiles(self) -> None:
        """Test that invalid SMILES returns None."""
        mol = parse_smiles("invalid_smiles_string")
        assert mol is None

    def test_parse_empty_string(self) -> None:
        """Test that empty string returns None."""
        mol = parse_smiles("")
        assert mol is None

    def test_parse_single_atom(self) -> None:
        """Test parsing single atom molecules."""
        mol = parse_smiles(METHANE)
        assert mol is not None
        assert mol.GetNumAtoms() == 1

    def test_parse_water(self) -> None:
        """Test parsing water molecule."""
        mol = parse_smiles(WATER)
        assert mol is not None
        assert mol.GetNumAtoms() == 1  # Only O, H implicit

    def test_parse_aromatic_ring(self) -> None:
        """Test parsing aromatic SMILES."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        assert mol.GetNumAtoms() == 6

    def test_parse_double_bond(self) -> None:
        """Test parsing molecule with double bond."""
        mol = parse_smiles(ETHENE)
        assert mol is not None
        assert mol.GetNumAtoms() == 2

    def test_parse_triple_bond(self) -> None:
        """Test parsing molecule with triple bond."""
        mol = parse_smiles(ETHYNE)
        assert mol is not None
        assert mol.GetNumAtoms() == 2

    def test_parse_ring(self) -> None:
        """Test parsing cyclic molecule."""
        mol = parse_smiles(CYCLOHEXANE)
        assert mol is not None
        assert mol.GetNumAtoms() == 6

    def test_molecule_has_2d_coords(self) -> None:
        """Test that parsed molecules have 2D coordinates."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        conf = mol.GetConformer()
        assert conf is not None
        pos = conf.GetAtomPosition(0)
        assert pos.x != 0 or pos.y != 0

    @pytest.mark.parametrize("name,smiles", list(SMILES_TEST_CASES.items()))  # type: ignore[misc]
    def test_parse_all_fixtures(self, name: str, smiles: str) -> None:
        """Test parsing all fixture molecules."""
        mol = parse_smiles(smiles)
        assert mol is not None, f"Failed to parse {name}: {smiles}"


class TestParseSdf:
    """Tests for SDF parsing."""

    def test_parse_ethanol_sdf(self) -> None:
        """Test parsing ethanol SDF file."""
        sdf_content = (FIXTURES_DIR / "ethanol.sdf").read_text()
        mol = parse_sdf(sdf_content)
        assert mol is not None
        assert isinstance(mol, Mol)

    def test_parse_benzene_sdf(self) -> None:
        """Test parsing benzene SDF file."""
        sdf_content = (FIXTURES_DIR / "benzene.sdf").read_text()
        mol = parse_sdf(sdf_content)
        assert mol is not None
        assert mol.GetNumAtoms() == 12  # Including hydrogens

    def test_parse_invalid_sdf(self) -> None:
        """Test that invalid SDF content returns None."""
        mol = parse_sdf("not valid sdf content")
        assert mol is None

    def test_parse_empty_sdf(self) -> None:
        """Test that empty SDF returns None."""
        mol = parse_sdf("")
        assert mol is None

    def test_sdf_preserves_coordinates(self) -> None:
        """Test that SDF parsing preserves 3D coordinates."""
        sdf_content = (FIXTURES_DIR / "ethanol.sdf").read_text()
        mol = parse_sdf(sdf_content)
        assert mol is not None
        conf = mol.GetConformer()
        pos = conf.GetAtomPosition(0)
        assert abs(pos.x - 1.0369) < 0.001
        assert abs(pos.y - (-0.0395)) < 0.001

    def test_sdf_atom_count(self) -> None:
        """Test correct atom count from SDF."""
        sdf_content = (FIXTURES_DIR / "ethanol.sdf").read_text()
        mol = parse_sdf(sdf_content)
        assert mol is not None
        assert mol.GetNumAtoms() == 9  # C, C, O, and 6 H


class TestNameToSmiles:
    """Tests for molecule name to SMILES conversion."""

    def test_placeholder(self) -> None:
        """Placeholder test for name conversion."""
        pass


class TestChemblToSmiles:
    """Tests for ChEMBL ID to SMILES conversion."""

    def test_placeholder(self) -> None:
        """Placeholder test for ChEMBL lookup."""
        pass
