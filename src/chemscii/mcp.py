"""MCP server for chemscii molecule rendering."""

from __future__ import annotations

import io
import sys
from typing import Literal

from mcp.server.fastmcp import FastMCP

from chemscii.cli import detect_input_type, parse_input
from chemscii.parsers.molecule import parse_smiles
from chemscii.renderers.ascii import AsciiRenderer
from chemscii.renderers.magic import AsciiMagicRenderer
from chemscii.renderers.unicode import UnicodeRenderer

RendererType = Literal["ascii", "unicode", "magic"]

mcp = FastMCP("chemscii")


def _resolve_smiles(molecule: str) -> str | None:
    """Resolve molecule input to SMILES string.

    Args:
        molecule: SMILES string, molecule name, ChEMBL ID, or SDF content.

    Returns:
        SMILES string if resolution succeeds, None otherwise.
    """
    from rdkit.rdBase import BlockLogs

    # Check if it looks like SDF content (multi-line with atom block markers)
    if "\n" in molecule and ("V2000" in molecule or "V3000" in molecule):
        from rdkit import Chem

        from chemscii.parsers.molecule import parse_sdf

        mol = parse_sdf(molecule)
        if mol is not None:
            return str(Chem.MolToSmiles(mol))
        return None

    # Use existing detection logic for SMILES/name/ChEMBL
    with BlockLogs():
        input_type, normalized = detect_input_type(molecule)

    return parse_input(input_type, normalized)


def _render(
    smiles: str,
    renderer: RendererType,
    width: int,
    height: int,
    columns: int,
    escape_codes: bool,
) -> str:
    """Render a molecule using the specified renderer.

    Args:
        smiles: SMILES string to render.
        renderer: Renderer type to use.
        width: Canvas width for ascii/unicode renderers.
        height: Canvas height for ascii/unicode renderers.
        columns: Output width for magic renderer.
        escape_codes: Include escape codes for color rendering.

    Returns:
        ASCII/Unicode art representation of the molecule.
    """
    mol = parse_smiles(smiles)
    if mol is None:
        raise ValueError(f"Failed to parse SMILES: {smiles}")

    # Capture stdout since renderers print to stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        r: AsciiRenderer | UnicodeRenderer | AsciiMagicRenderer
        if renderer == "ascii":
            r = AsciiRenderer(width=width, height=height)
        elif renderer == "unicode":
            r = UnicodeRenderer(width=width, height=height)
        else:
            r = AsciiMagicRenderer(columns=columns, codes=escape_codes)
        r.render_molecule(mol)
        result: str = repr(sys.stdout.getvalue())

        return result
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout


@mcp.tool()  # type: ignore[misc]
def render_molecule(
    molecule: str,
    renderer: RendererType = "magic",
    width: int = 60,
    height: int = 30,
    columns: int = 80,
    escape_codes: bool = False,
) -> str:
    """Render a chemical structure as ASCII/Unicode art.

    Args:
        molecule: SMILES string, molecule name, ChEMBL ID, or SDF content.
        renderer: Renderer type: "ascii", "unicode", or "magic" (default).
        width: Canvas width for ascii/unicode renderers.
        height: Canvas height for ascii/unicode renderers.
        columns: Output width for magic renderer.
        escape_codes: Include escape codes for color rendering.

    Returns:
        ASCII/Unicode art representation of the molecule.
    """
    smiles = _resolve_smiles(molecule)
    if smiles is None:
        return f"Error: Could not parse molecule input: {molecule}"

    try:
        return _render(smiles, renderer, width, height, columns, escape_codes)
    except Exception as e:
        return f"Error rendering molecule: {e}"


def run_server(
    renderer: RendererType = "magic",
    width: int = 60,
    height: int = 30,
    columns: int = 80,
    escape_codes: bool = False,
) -> None:
    """Run the MCP server with optional default settings.

    Args:
        renderer: Default renderer type.
        width: Default canvas width for ascii/unicode renderers.
        height: Default canvas height for ascii/unicode renderers.
        columns: Default output width for magic renderer.
        escape_codes: Default for including escape codes.
    """
    # Store defaults that could be used by the tool
    # For now, the tool uses its own defaults but this allows future extension
    _ = (renderer, width, height, columns, escape_codes)

    mcp.run()
