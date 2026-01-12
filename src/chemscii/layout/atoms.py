"""Atom positioning for 2D layout."""

from __future__ import annotations

from rdkit.Chem import Kekulize, Mol, rdDepictor


class AtomLayout:
    """Handles 2D positioning of atoms in a molecule."""

    def __init__(self, molecule: Mol) -> None:
        """Initialize atom layout for a molecule.

        Args:
            molecule: An RDKit Mol object with 2D coordinates.
        """
        self.molecule = molecule
        Kekulize(self.molecule)
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(self.molecule, useRingTemplates=True)
        self.positions: list[tuple[float, float]] = []
        self._symbols: list[str] = []

    def compute_positions(self) -> list[tuple[float, float]]:
        """Compute 2D coordinates for all atoms.

        Returns:
            List of (x, y) coordinate tuples for each atom.
        """
        conformer = self.molecule.GetConformer()
        self.positions = []
        self._symbols = []

        for atom in self.molecule.GetAtoms():
            idx = atom.GetIdx()
            pos = conformer.GetAtomPosition(idx)
            self.positions.append((pos.x, pos.y))
            self._symbols.append(atom.GetSymbol())

        return self.positions

    def get_symbols(self) -> list[str]:
        """Get element symbols for all atoms.

        Must be called after compute_positions().

        Returns:
            List of element symbols (e.g., ['C', 'C', 'O']).
        """
        return self._symbols

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box of atom positions.

        Must be called after compute_positions().

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if not self.positions:
            return (0.0, 0.0, 0.0, 0.0)

        xs = [p[0] for p in self.positions]
        ys = [p[1] for p in self.positions]
        return (min(xs), min(ys), max(xs), max(ys))
