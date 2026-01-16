"""Basic ASCII renderer for chemical structures."""

from __future__ import annotations

from chemscii.renderers.base import BaseRenderer

# ANSI color codes
_COLORS: dict[str, str] = {
    "red": "\033[91m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
}

# Element to color mapping
_ELEMENT_COLORS: dict[str, str] = {
    "O": "red",
    "N": "blue",
    "S": "yellow",
    "F": "cyan",
    "Cl": "cyan",
    "Br": "cyan",
    "I": "cyan",
}


class AsciiRenderer(BaseRenderer):
    """Renders chemical structures using basic ASCII characters."""

    _HORIZONTAL = "-"
    _VERTICAL = "|"
    _DIAG_UP = "/"
    _DIAG_DOWN = "\\"
    _DOUBLE = "="
    _TRIPLE = "#"

    def __init__(
        self,
        width: int = -1,
        height: int = -1,
        padding: int = 2,
        color: bool = True,
    ) -> None:
        """Initialize the ASCII renderer.

        Args:
            width: Canvas width in characters (-1 for auto).
            height: Canvas height in characters (-1 for auto).
            padding: Padding around the molecule in characters.
            color: Whether to colorize element symbols.
        """
        super().__init__(width=width, height=height, padding=padding)
        self.color = color

    def _draw_atom(self, canvas: list[list[str]], x: int, y: int, symbol: str) -> None:
        """Draw an atom symbol on the canvas with optional color.

        Args:
            canvas: The character canvas.
            x: Canvas x coordinate.
            y: Canvas y coordinate.
            symbol: Element symbol to draw.
        """
        if self.color and symbol in _ELEMENT_COLORS:
            color_name = _ELEMENT_COLORS[symbol]
            color_code = _COLORS[color_name]
            reset_code = _COLORS["reset"]
            # Apply color to the entire symbol
            for i, char in enumerate(symbol[:2]):
                px = x + i
                if 0 <= y < self.height and 0 <= px < self.width:
                    canvas[y][px] = f"{color_code}{char}{reset_code}"
        else:
            # Default behavior without color
            for i, char in enumerate(symbol[:2]):
                px = x + i
                if 0 <= y < self.height and 0 <= px < self.width:
                    canvas[y][px] = char
