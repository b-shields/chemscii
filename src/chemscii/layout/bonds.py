"""Bond positioning for 2D layout."""

from __future__ import annotations

from rdkit.Chem import BondType, Mol

# Map RDKit bond types to integer bond orders
_BOND_ORDER_MAP: dict[BondType, int] = {
    BondType.SINGLE: 1,
    BondType.DOUBLE: 2,
    BondType.TRIPLE: 3,
    BondType.AROMATIC: 1,  # Render aromatic as single for simplicity
}


class BondLayout:
    """Handles 2D positioning of bonds in a molecule."""

    def __init__(
        self, molecule: Mol, atom_positions: list[tuple[float, float]]
    ) -> None:
        """Initialize bond layout for a molecule.

        Args:
            molecule: An RDKit Mol object.
            atom_positions: List of (x, y) coordinates for each atom.
        """
        self.molecule = molecule
        self.atom_positions = atom_positions
        self._bond_lines: list[tuple[tuple[float, float], tuple[float, float], int]] = (
            []
        )

    def compute_bond_lines(
        self,
    ) -> list[tuple[tuple[float, float], tuple[float, float], int]]:
        """Compute line segments for all bonds.

        Returns:
            List of ((x1, y1), (x2, y2), bond_order) tuples.
        """
        self._bond_lines = []

        for bond in self.molecule.GetBonds():
            begin_idx = bond.GetBeginAtomIdx()
            end_idx = bond.GetEndAtomIdx()

            if begin_idx >= len(self.atom_positions) or end_idx >= len(
                self.atom_positions
            ):
                continue

            start_pos = self.atom_positions[begin_idx]
            end_pos = self.atom_positions[end_idx]

            bond_type = bond.GetBondType()
            bond_order = _BOND_ORDER_MAP.get(bond_type, 1)

            self._bond_lines.append((start_pos, end_pos, bond_order))

        return self._bond_lines

    def get_aromatic_bonds(self) -> list[tuple[int, int]]:
        """Get indices of aromatic bonds.

        Returns:
            List of (begin_atom_idx, end_atom_idx) tuples for aromatic bonds.
        """
        aromatic = []
        for bond in self.molecule.GetBonds():
            if bond.GetIsAromatic():
                aromatic.append((bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()))
        return aromatic
