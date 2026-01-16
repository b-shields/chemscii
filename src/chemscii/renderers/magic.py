"""ASCII magic renderer for chemical structures using image conversion."""

from __future__ import annotations

import io

from ascii_magic import AsciiArt
from PIL import Image
from rdkit.Chem import Kekulize, Mol, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D


class AsciiMagicRenderer:
    """Renders chemical structures as ASCII art via image conversion.

    This renderer uses RDKit to draw the molecule as an image, then converts
    the image to ASCII art using the ascii_magic library.
    """

    def __init__(self, columns: int = 120, codes: bool = True) -> None:
        """Initialize the renderer.

        Args:
            columns: Width of the ASCII art output in characters.
            codes: Include escape codes.
        """
        self.columns = columns
        self.codes = codes

    def render_molecule(self, mol: Mol) -> str:
        """Render a molecule as ASCII art.

        Args:
            mol: An RDKit Mol object.

        Returns:
            ASCII art representation of the molecule.
        """
        img = self._mol_to_image(mol)
        art = AsciiArt.from_pillow_image(img)
        if self.codes:
            txt: str = art.to_ascii(self.columns)
            print(repr(txt))
        else:
            txt = art.to_terminal(self.columns)
        return txt

    def _mol_to_image(
        self, mol: Mol, mol_size: tuple[int, int] = (300, 300)
    ) -> Image.Image:
        """Convert a molecule to a PIL Image.

        Args:
            mol: An RDKit Mol object.
            mol_size: Width and height of the output image in pixels.

        Returns:
            PIL Image of the rendered molecule.
        """
        # Standardize molecule
        Kekulize(mol)
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(mol, useRingTemplates=True)

        # Geneate image
        drawer = rdMolDraw2D.MolDraw2DCairo(*mol_size)
        rdMolDraw2D.SetDarkMode(drawer)
        drawer.drawOptions().padding = 0.0
        drawer.drawOptions().bondLineWidth = 5
        drawer.drawOptions().minFontSize = 20
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        bio = io.BytesIO(drawer.GetDrawingText())
        return Image.open(bio)
