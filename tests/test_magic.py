"""Tests for chemscii.renderers.magic module."""

from PIL import Image

from chemscii.parsers.molecule import parse_smiles
from chemscii.renderers.magic import AsciiMagicRenderer
from tests.fixtures.molecules import (
    BENZENE,
    CAFFEINE,
    ETHANOL,
    ETHENE,
    ETHYNE,
    METHANE,
)


class TestAsciiMagicRenderer:
    """Tests for ASCII magic rendering via image conversion."""

    def test_init_default_columns(self) -> None:
        """Test renderer initializes with default columns."""
        renderer = AsciiMagicRenderer()
        assert renderer.columns == 120

    def test_init_custom_columns(self) -> None:
        """Test renderer initializes with custom columns."""
        renderer = AsciiMagicRenderer(columns=80)
        assert renderer.columns == 80

    def test_render_molecule_returns_string(self) -> None:
        """Test that render_molecule returns a string."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=60)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)

    def test_render_molecule_non_empty(self) -> None:
        """Test that render_molecule returns non-empty output."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=60)
        result = renderer.render_molecule(mol)
        assert len(result) > 0

    def test_render_benzene(self) -> None:
        """Test rendering benzene ring."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=80)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_methane(self) -> None:
        """Test rendering single atom molecule."""
        mol = parse_smiles(METHANE)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=40)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_double_bond(self) -> None:
        """Test rendering molecule with double bond."""
        mol = parse_smiles(ETHENE)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=60)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_triple_bond(self) -> None:
        """Test rendering molecule with triple bond."""
        mol = parse_smiles(ETHYNE)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=60)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_complex_molecule(self) -> None:
        """Test rendering complex molecule like caffeine."""
        mol = parse_smiles(CAFFEINE)
        assert mol is not None
        renderer = AsciiMagicRenderer(columns=100)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_mol_to_image_returns_pil_image(self) -> None:
        """Test that _mol_to_image returns a PIL Image."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        renderer = AsciiMagicRenderer()
        img = renderer._mol_to_image(mol)
        assert isinstance(img, Image.Image)

    def test_mol_to_image_default_size(self) -> None:
        """Test _mol_to_image with default size."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        renderer = AsciiMagicRenderer()
        img = renderer._mol_to_image(mol)
        assert img.size == (300, 300)

    def test_mol_to_image_custom_size(self) -> None:
        """Test _mol_to_image with custom size."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        renderer = AsciiMagicRenderer()
        img = renderer._mol_to_image(mol, mol_size=(500, 500))
        assert img.size == (500, 500)

    def test_mol_to_image_rectangular_size(self) -> None:
        """Test _mol_to_image with rectangular dimensions."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        renderer = AsciiMagicRenderer()
        img = renderer._mol_to_image(mol, mol_size=(400, 200))
        assert img.size == (400, 200)

    def test_different_column_widths_produce_different_output(self) -> None:
        """Test that different column widths produce different output lengths."""
        mol = parse_smiles(BENZENE)
        assert mol is not None

        renderer_small = AsciiMagicRenderer(columns=40)
        renderer_large = AsciiMagicRenderer(columns=120)

        result_small = renderer_small.render_molecule(mol)
        result_large = renderer_large.render_molecule(mol)

        # Larger column width should generally produce longer lines
        small_max_line = max(len(line) for line in result_small.split("\n"))
        large_max_line = max(len(line) for line in result_large.split("\n"))
        assert small_max_line <= large_max_line
