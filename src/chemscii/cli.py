"""Command-line interface for chemscii."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import typer
from rich.console import Console
from rich.panel import Panel

from chemscii.parsers.chembl import chembl_to_smiles
from chemscii.parsers.molecule import parse_sdf, parse_smiles
from chemscii.parsers.name import name_to_smiles
from chemscii.renderers.ascii import AsciiRenderer
from chemscii.renderers.magic import AsciiMagicRenderer
from chemscii.renderers.unicode import UnicodeRenderer

app = typer.Typer(
    name="chemscii",
    help="Render chemical structures as ASCII/Unicode art.",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True)

# Pattern for ChEMBL IDs
_CHEMBL_PATTERN = re.compile(r"^CHEMBL\d+$", re.IGNORECASE)

InputType = Literal["file", "chembl", "smiles", "name"]


def detect_input_type(value: str) -> tuple[InputType, str]:
    """Detect the type of molecular input.

    Args:
        value: The input string to analyze.

    Returns:
        A tuple of (input_type, normalized_value).
    """
    stripped = value.strip()

    # Check if it's a file path
    path = Path(stripped)
    if path.exists() and path.is_file():
        return "file", stripped

    # Check if it's a ChEMBL ID
    if _CHEMBL_PATTERN.match(stripped):
        return "chembl", stripped.upper()

    # Check if it's a valid SMILES
    mol = parse_smiles(stripped)
    if mol is not None:
        return "smiles", stripped

    # Default to name lookup
    return "name", stripped


def parse_input(input_type: InputType, value: str) -> str | None:
    """Parse input and return SMILES string.

    Args:
        input_type: The detected input type.
        value: The input value.

    Returns:
        SMILES string if parsing succeeds, None otherwise.
    """
    if input_type == "smiles":
        return value

    if input_type == "chembl":
        return chembl_to_smiles(value)

    if input_type == "name":
        return name_to_smiles(value)

    if input_type == "file":
        path = Path(value)
        content = path.read_text()
        suffix = path.suffix.lower()

        if suffix in (".sdf", ".mol"):
            mol = parse_sdf(content)
            if mol is not None:
                from rdkit import Chem

                return str(Chem.MolToSmiles(mol))
        elif suffix == ".smi":
            # SMILES file - take first line
            first_line = content.strip().split("\n")[0]
            smiles = first_line.split()[0] if first_line else None
            return smiles

    return None


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print("chemscii 0.1.0")
        raise typer.Exit()


@app.command()  # type: ignore[misc, unused-ignore]
def main(
    molecule: str = typer.Argument(
        ...,
        help="SMILES string, molecule name, ChEMBL ID, or file path.",
    ),
    ascii_mode: bool = typer.Option(
        False,
        "--ascii",
        "-a",
        help="Use ASCII character renderer.",
    ),
    unicode_mode: bool = typer.Option(
        False,
        "--unicode",
        "-u",
        help="Use Unicode box-drawing renderer.",
    ),
    magic_mode: bool = typer.Option(
        False,
        "--magic",
        "-m",
        help="Use image-to-ASCII magic renderer (default).",
    ),
    columns: int = typer.Option(
        50,
        "--columns",
        "-c",
        help="Output width for magic renderer.",
    ),
    width: int = typer.Option(
        60,
        "--width",
        "-w",
        help="Canvas width for ascii/unicode renderers.",
    ),
    height: int = typer.Option(
        30,
        "--height",
        "-H",
        help="Canvas height for ascii/unicode renderers.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Render a chemical structure as ASCII/Unicode art.

    Automatically detects input type: SMILES strings, molecule names,
    ChEMBL IDs, or structure files (.sdf, .mol, .smi).
    """
    from rdkit.rdBase import BlockLogs

    # Detect input type
    with BlockLogs():
        input_type, normalized = detect_input_type(molecule)

    # Parse to SMILES
    smiles = parse_input(input_type, normalized)
    if smiles is None:
        error_console.print(
            Panel(
                f"[red]Could not parse input:[/red] {molecule}\n\n"
                f"Detected as: [yellow]{input_type}[/yellow]\n\n"
                "Examples of valid inputs:\n"
                "  • SMILES: CCO, c1ccccc1, CC(=O)O\n"
                "  • Names: aspirin, caffeine, benzene\n"
                "  • ChEMBL: CHEMBL25, CHEMBL113\n"
                "  • Files: molecule.sdf, compound.mol",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    # Parse SMILES to molecule
    mol = parse_smiles(smiles)
    if mol is None:
        error_console.print(
            Panel(
                f"[red]Failed to parse SMILES:[/red] {smiles}",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    # Determine renderer
    renderer_count = sum([ascii_mode, unicode_mode, magic_mode])
    if renderer_count > 1:
        error_console.print(
            Panel(
                "[red]Only one renderer can be selected.[/red]\n"
                "Use --ascii, --unicode, or --magic (not multiple).",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    # Render molecule
    if ascii_mode:
        ascii_renderer = AsciiRenderer(width=width, height=height)
        ascii_renderer.render_molecule(mol)
    elif unicode_mode:
        unicode_renderer = UnicodeRenderer(width=width, height=height)
        unicode_renderer.render_molecule(mol)
    else:
        # Default to magic
        magic_renderer = AsciiMagicRenderer(columns=columns)
        magic_renderer.render_molecule(mol)


if __name__ == "__main__":
    app()
