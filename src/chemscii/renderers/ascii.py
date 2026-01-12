"""Basic ASCII renderer for chemical structures."""

from __future__ import annotations

from chemscii.renderers.base import BaseRenderer


class AsciiRenderer(BaseRenderer):
    """Renders chemical structures using basic ASCII characters."""

    _HORIZONTAL = "."
    _VERTICAL = ":"
    _DIAG_UP = "."
    _DIAG_DOWN = "."
    _DOUBLE = "$"
    _TRIPLE = "#"
