"""Enhanced Unicode renderer for chemical structures."""

from __future__ import annotations

import math

from chemscii.renderers.base import BaseRenderer


class UnicodeRenderer(BaseRenderer):
    """Renders chemical structures using Unicode box-drawing characters."""

    _HORIZONTAL = "─"
    _VERTICAL = "│"
    _DIAG_UP = "╱"
    _DIAG_DOWN = "╲"
    _DOUBLE = "═"
    _DOUBLE_VERTICAL = "║"
    _TRIPLE = "≡"

    def _get_bond_char(self, angle: float, order: int) -> str:
        """Get the appropriate bond character for an angle.

        Args:
            angle: Angle in radians.
            order: Bond order.

        Returns:
            Character to use for the bond.
        """
        if order == 3:
            return self._TRIPLE

        # Normalize angle to [0, pi)
        norm_angle = angle % math.pi

        if order == 2:
            # Use vertical double bond for near-vertical angles
            if 3 * math.pi / 8 <= norm_angle < 5 * math.pi / 8:
                return self._DOUBLE_VERTICAL
            return self._DOUBLE

        # Single bond character based on angle
        if norm_angle < math.pi / 8 or norm_angle >= 7 * math.pi / 8:
            return self._HORIZONTAL
        elif norm_angle < 3 * math.pi / 8:
            return self._DIAG_DOWN
        elif norm_angle < 5 * math.pi / 8:
            return self._VERTICAL
        else:
            return self._DIAG_UP
