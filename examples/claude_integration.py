"""Example of integrating chemscii with Claude/LLM workflows."""

from chemscii.layout import AtomLayout, BondLayout
from chemscii.parsers import name_to_smiles, parse_smiles
from chemscii.renderers import UnicodeRenderer


def render_molecule(input_str: str) -> str:
    """Render a molecule from SMILES or name.

    Args:
        input_str: Either a SMILES string or molecule name.

    Returns:
        Unicode art representation of the molecule.
    """
    # Try parsing as SMILES first
    molecule = parse_smiles(input_str)

    if molecule is None:
        # Try converting name to SMILES
        smiles = name_to_smiles(input_str)
        if smiles:
            molecule = parse_smiles(smiles)

    if molecule is None:
        return f"Could not parse: {input_str}"

    # Generate layout
    atom_layout = AtomLayout(molecule)
    positions = atom_layout.compute_positions()

    bond_layout = BondLayout(molecule, positions)
    bonds = bond_layout.compute_bond_lines()

    # Render with Unicode for better terminal display
    renderer = UnicodeRenderer(width=60, height=30)
    return renderer.render(positions, bonds, [])


def main() -> None:
    """Demo Claude integration workflow."""
    # Example molecules that might be discussed in an LLM conversation
    molecules = [
        "CCO",  # Ethanol
        "c1ccccc1",  # Benzene
        "CC(=O)O",  # Acetic acid
    ]

    for mol in molecules:
        print(f"SMILES: {mol}")
        print(render_molecule(mol))
        print("-" * 60)


if __name__ == "__main__":
    main()
