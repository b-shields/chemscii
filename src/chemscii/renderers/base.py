"""Base renderer for chemical structures."""

from __future__ import annotations

import math
from abc import ABC

from rdkit.Chem import Mol

from chemscii.layout import AtomLayout, BondLayout


class BaseRenderer(ABC):
    """Abstract base class for chemical structure renderers."""

    # Bond characters - subclasses must define these
    _HORIZONTAL: str
    _VERTICAL: str
    _DIAG_UP: str
    _DIAG_DOWN: str
    _DOUBLE: str
    _TRIPLE: str

    def __init__(self, width: int = -1, height: int = -1, padding: int = 2) -> None:
        """Initialize the renderer.

        Args:
            width: Canvas width in characters (-1 for auto).
            height: Canvas height in characters (-1 for auto).
            padding: Padding around the molecule in characters.
        """
        self._auto_width = width == -1
        self.width = width
        self._auto_height = height == -1
        self.height = height
        self.padding = padding

    def render_molecule(self, mol: Mol) -> str:
        """Render a molecule as text art.

        Args:
            mol: An RDKit Mol object.

        Returns:
            Text art representation of the molecule.
        """
        atom_layout = AtomLayout(mol)
        atom_positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, atom_positions)
        bond_lines = bond_layout.compute_bond_lines()
        atom_symbols = atom_layout.get_symbols()

        return self.render(atom_positions, bond_lines, atom_symbols)

    def render(
        self,
        atom_positions: list[tuple[float, float]],
        bond_lines: list[tuple[tuple[float, float], tuple[float, float], int]],
        atom_symbols: list[str],
    ) -> str:
        """Render atoms, bonds, and symbols as text art.

        Args:
            atom_positions: List of (x, y) coordinates for atoms.
            bond_lines: List of ((x1, y1), (x2, y2), bond_order) tuples.
            atom_symbols: List of element symbols for each atom.

        Returns:
            Text art representation of the molecule.
        """
        if not atom_positions:
            return ""

        if self._auto_width:
            self.width = len(atom_symbols) + 10
        if self._auto_height:
            self.height = len(atom_symbols) + 10

        # Create canvas
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Calculate transformation from molecular coords to canvas coords
        transform = self._compute_transform(atom_positions)

        # Draw bonds first (so atoms overlay them)
        for start, end, order in bond_lines:
            self._draw_bond(canvas, start, end, order, transform)

        # Draw atoms
        for i, (x, y) in enumerate(atom_positions):
            cx, cy = self._transform_point(x, y, transform)
            if 0 <= cy < self.height and 0 <= cx < self.width:
                symbol = atom_symbols[i] if i < len(atom_symbols) else "?"
                self._draw_atom(canvas, cx, cy, symbol)

        # Convert canvas to string
        return "\n".join("".join(row).rstrip() for row in canvas).rstrip()

    def _compute_transform(
        self, positions: list[tuple[float, float]]
    ) -> tuple[float, float, float, float]:
        """Compute transformation parameters from molecular to canvas coords.

        Args:
            positions: List of (x, y) molecular coordinates.

        Returns:
            Tuple of (scale, offset_x, offset_y, reserved).
        """
        if not positions:
            return (1.0, 0.0, 0.0, 1.0)

        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        mol_width = max_x - min_x
        mol_height = max_y - min_y

        # Available canvas space (accounting for padding and atom labels)
        avail_width = self.width - 2 * self.padding - 2
        avail_height = self.height - 2 * self.padding

        # Calculate scale to fit molecule in canvas
        if mol_width > 0 and mol_height > 0:
            scale_x = avail_width / mol_width
            scale_y = avail_height / mol_height
            scale = min(scale_x, scale_y)
        elif mol_width > 0:
            scale = avail_width / mol_width
        elif mol_height > 0:
            scale = avail_height / mol_height
        else:
            scale = 1.0

        # Center the molecule
        scaled_width = mol_width * scale
        scaled_height = mol_height * scale
        offset_x = self.padding + (avail_width - scaled_width) / 2 - min_x * scale
        offset_y = self.padding + (avail_height - scaled_height) / 2 - min_y * scale

        return (scale, offset_x, offset_y, 1.0)

    def _transform_point(
        self, x: float, y: float, transform: tuple[float, float, float, float]
    ) -> tuple[int, int]:
        """Transform molecular coordinates to canvas coordinates.

        Args:
            x: Molecular x coordinate.
            y: Molecular y coordinate.
            transform: Transformation parameters.

        Returns:
            Canvas (x, y) coordinates as integers.
        """
        scale, offset_x, offset_y, _ = transform
        cx = int(round(x * scale + offset_x))
        # Flip y-axis (canvas y increases downward)
        cy = int(round(self.height - 1 - (y * scale + offset_y)))
        return (cx, cy)

    def _draw_atom(self, canvas: list[list[str]], x: int, y: int, symbol: str) -> None:
        """Draw an atom symbol on the canvas.

        Args:
            canvas: The character canvas.
            x: Canvas x coordinate.
            y: Canvas y coordinate.
            symbol: Element symbol to draw.
        """
        # Draw the symbol (up to 2 characters)
        for i, char in enumerate(symbol[:2]):
            px = x + i
            if 0 <= y < self.height and 0 <= px < self.width:
                canvas[y][px] = char

    def _draw_bond(
        self,
        canvas: list[list[str]],
        start: tuple[float, float],
        end: tuple[float, float],
        order: int,
        transform: tuple[float, float, float, float],
    ) -> None:
        """Draw a bond line on the canvas.

        Args:
            canvas: The character canvas.
            start: Starting molecular coordinates.
            end: Ending molecular coordinates.
            order: Bond order (1, 2, or 3).
            transform: Transformation parameters.
        """
        x1, y1 = self._transform_point(start[0], start[1], transform)
        x2, y2 = self._transform_point(end[0], end[1], transform)

        # Use Bresenham-like line drawing
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return

        # Determine bond character based on angle
        angle = math.atan2(dy, dx)
        bond_char = self._get_bond_char(angle, order)

        # Draw line
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            x = int(round(x1 + dx * t))
            y = int(round(y1 + dy * t))

            if 0 <= y < self.height and 0 <= x < self.width:
                # Don't overwrite existing atom symbols
                if canvas[y][x] == " ":
                    canvas[y][x] = bond_char

    def _get_bond_char(self, angle: float, order: int) -> str:
        """Get the appropriate bond character for an angle.

        Args:
            angle: Angle in radians.
            order: Bond order.

        Returns:
            Character to use for the bond.
        """
        if order == 2:
            return self._DOUBLE
        elif order == 3:
            return self._TRIPLE

        # Normalize angle to [0, pi)
        angle = angle % math.pi

        # Determine character based on angle
        if angle < math.pi / 8 or angle >= 7 * math.pi / 8:
            return self._HORIZONTAL
        elif angle < 3 * math.pi / 8:
            return self._DIAG_DOWN
        elif angle < 5 * math.pi / 8:
            return self._VERTICAL
        else:
            return self._DIAG_UP
