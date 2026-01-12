"""Tests for chemscii.parsers module."""

from pathlib import Path

import pytest
from rdkit.Chem import Mol

from chemscii.parsers.chembl import chembl_to_smiles
from chemscii.parsers.molecule import parse_sdf, parse_smiles
from chemscii.parsers.name import name_to_smiles
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

    def test_common_molecule_water(self) -> None:
        """Test lookup of water."""
        smiles = name_to_smiles("water", use_pubchem=False)
        assert smiles == "O"

    def test_common_molecule_ethanol(self) -> None:
        """Test lookup of ethanol."""
        smiles = name_to_smiles("ethanol", use_pubchem=False)
        assert smiles == "CCO"

    def test_common_molecule_benzene(self) -> None:
        """Test lookup of benzene."""
        smiles = name_to_smiles("benzene", use_pubchem=False)
        assert smiles == "c1ccccc1"

    def test_common_molecule_aspirin(self) -> None:
        """Test lookup of aspirin."""
        smiles = name_to_smiles("aspirin", use_pubchem=False)
        assert smiles is not None
        assert "C(=O)O" in smiles  # Carboxylic acid group

    def test_case_insensitive(self) -> None:
        """Test that lookup is case insensitive."""
        assert name_to_smiles("Water", use_pubchem=False) == "O"
        assert name_to_smiles("WATER", use_pubchem=False) == "O"
        assert name_to_smiles("wAtEr", use_pubchem=False) == "O"

    def test_whitespace_handling(self) -> None:
        """Test that whitespace is stripped."""
        assert name_to_smiles("  water  ", use_pubchem=False) == "O"
        assert name_to_smiles("\tethanol\n", use_pubchem=False) == "CCO"

    def test_empty_string_returns_none(self) -> None:
        """Test that empty string returns None."""
        assert name_to_smiles("", use_pubchem=False) is None
        assert name_to_smiles("   ", use_pubchem=False) is None

    def test_unknown_molecule_without_pubchem(self) -> None:
        """Test that unknown molecule returns None without PubChem."""
        smiles = name_to_smiles("unknownmolecule12345", use_pubchem=False)
        assert smiles is None

    def test_multi_word_name(self) -> None:
        """Test lookup of multi-word molecule names."""
        smiles = name_to_smiles("acetic acid", use_pubchem=False)
        assert smiles == "CC(=O)O"

    def test_carbon_dioxide(self) -> None:
        """Test lookup of carbon dioxide."""
        smiles = name_to_smiles("carbon dioxide", use_pubchem=False)
        assert smiles == "O=C=O"

    @pytest.mark.network  # type: ignore[misc]
    def test_pubchem_lookup(self) -> None:
        """Test PubChem lookup for unknown molecule."""
        # Penicillin G - not in local dict, requires PubChem
        smiles = name_to_smiles("penicillin G", use_pubchem=True)
        # May be None if network unavailable, but if found should be valid
        if smiles is not None:
            mol = parse_smiles(smiles)
            assert mol is not None


class TestChemblToSmiles:
    """Tests for ChEMBL ID to SMILES conversion."""

    def test_cached_aspirin(self) -> None:
        """Test lookup of aspirin (CHEMBL25)."""
        smiles = chembl_to_smiles("CHEMBL25", use_api=False)
        assert smiles is not None
        assert "C(=O)O" in smiles  # Carboxylic acid group

    def test_cached_caffeine(self) -> None:
        """Test lookup of caffeine (CHEMBL113)."""
        smiles = chembl_to_smiles("CHEMBL113", use_api=False)
        assert smiles is not None
        mol = parse_smiles(smiles)
        assert mol is not None

    def test_cached_ethanol(self) -> None:
        """Test lookup of ethanol (CHEMBL521)."""
        smiles = chembl_to_smiles("CHEMBL521", use_api=False)
        assert smiles == "CCO"

    def test_cached_water(self) -> None:
        """Test lookup of water (CHEMBL27732)."""
        smiles = chembl_to_smiles("CHEMBL27732", use_api=False)
        assert smiles == "O"

    def test_case_insensitive(self) -> None:
        """Test that lookup is case insensitive."""
        assert chembl_to_smiles("chembl25", use_api=False) is not None
        assert chembl_to_smiles("ChEmBl25", use_api=False) is not None
        assert chembl_to_smiles("CHEMBL25", use_api=False) is not None

    def test_whitespace_handling(self) -> None:
        """Test that whitespace is stripped."""
        assert chembl_to_smiles("  CHEMBL25  ", use_api=False) is not None
        assert chembl_to_smiles("\tCHEMBL521\n", use_api=False) == "CCO"

    def test_empty_string_returns_none(self) -> None:
        """Test that empty string returns None."""
        assert chembl_to_smiles("", use_api=False) is None
        assert chembl_to_smiles("   ", use_api=False) is None

    def test_invalid_format_returns_none(self) -> None:
        """Test that invalid ChEMBL ID format returns None."""
        assert chembl_to_smiles("25", use_api=False) is None
        assert chembl_to_smiles("CHEMBL", use_api=False) is None
        assert chembl_to_smiles("CHEMBLabc", use_api=False) is None
        assert chembl_to_smiles("aspirin", use_api=False) is None

    def test_unknown_id_without_api(self) -> None:
        """Test that unknown ID returns None without API."""
        smiles = chembl_to_smiles("CHEMBL999999999", use_api=False)
        assert smiles is None

    @pytest.mark.network  # type: ignore[misc]
    def test_api_lookup(self) -> None:
        """Test ChEMBL API lookup for compound not in cache."""
        # Penicillin V - not in local cache
        smiles = chembl_to_smiles("CHEMBL615", use_api=True)
        # May be None if network unavailable, but if found should be valid
        if smiles is not None:
            mol = parse_smiles(smiles)
            assert mol is not None
