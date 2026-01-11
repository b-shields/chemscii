"""Parse SMILES and SDF molecular formats."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import Mol, rdDepictor


def parse_smiles(smiles: str) -> Mol | None:
    """Parse a SMILES string into a molecule object.

    Args:
        smiles: A SMILES string representation of a molecule.

    Returns:
        An RDKit Mol object, or None if parsing fails.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        rdDepictor.Compute2DCoords(mol)
    return mol


def parse_sdf(sdf_content: str) -> Mol | None:
    """Parse SDF file content into a molecule object.

    Args:
        sdf_content: The contents of an SDF file as a string.

    Returns:
        An RDKit Mol object, or None if parsing fails.
    """
    mol = Chem.MolFromMolBlock(sdf_content)
    if mol is not None:
        rdDepictor.Compute2DCoords(mol)
    return mol
