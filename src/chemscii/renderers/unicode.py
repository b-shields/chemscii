"""Enhanced Unicode renderer for chemical structures."""

from __future__ import annotations

from chemscii.renderers.base import BaseRenderer


class UnicodeRenderer(BaseRenderer):
    """Renders chemical structures using Unicode box-drawing characters."""

    _HORIZONTAL = "·"
    _VERTICAL = ":"
    _DIAG_UP = "·"
    _DIAG_DOWN = "·"
    _DOUBLE = "$"
    _TRIPLE = "#"
