"""Basic usage example for chemscii."""

from chemscii.layout import AtomLayout, BondLayout
from chemscii.parsers import parse_smiles
from chemscii.renderers import AsciiRenderer


def main() -> None:
    """Demonstrate basic chemscii usage."""
    # Example: Render ethanol (CCO)
    smiles = "CCO"

    # Parse the SMILES string
    molecule = parse_smiles(smiles)

    # Compute 2D layout
    atom_layout = AtomLayout(molecule)
    positions = atom_layout.compute_positions()

    bond_layout = BondLayout(molecule, positions)
    bonds = bond_layout.compute_bond_lines()

    # Render as ASCII
    renderer = AsciiRenderer(width=40, height=20)
    ascii_art = renderer.render(positions, bonds, ["C", "C", "O"])

    print(ascii_art)


if __name__ == "__main__":
    main()
