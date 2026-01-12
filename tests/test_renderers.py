"""Tests for chemscii.renderers module."""

import math

from chemscii.layout.atoms import AtomLayout
from chemscii.layout.bonds import BondLayout
from chemscii.parsers.molecule import parse_smiles
from chemscii.renderers.ascii import AsciiRenderer
from chemscii.renderers.unicode import UnicodeRenderer
from tests.fixtures.molecules import BENZENE, ETHANOL, ETHENE, ETHYNE, METHANE


class TestAsciiRenderer:
    """Tests for ASCII rendering."""

    def test_render_empty_positions(self) -> None:
        """Test rendering with empty positions."""
        renderer = AsciiRenderer()
        result = renderer.render([], [], [])
        assert result == ""

    def test_render_single_atom(self) -> None:
        """Test rendering a single atom."""
        renderer = AsciiRenderer(width=20, height=10)
        result = renderer.render([(0.0, 0.0)], [], ["C"])
        assert "C" in result

    def test_render_returns_string(self) -> None:
        """Test that render returns a string."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert isinstance(result, str)

    def test_render_contains_atoms(self) -> None:
        """Test that rendered output contains atom symbols."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        assert "O" in result

    def test_render_benzene(self) -> None:
        """Test rendering benzene ring."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_methane(self) -> None:
        """Test rendering single atom molecule."""
        mol = parse_smiles(METHANE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=20, height=10)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result

    def test_custom_dimensions(self) -> None:
        """Test renderer with custom dimensions."""
        renderer = AsciiRenderer(width=100, height=50, padding=5)
        assert renderer.width == 100
        assert renderer.height == 50
        assert renderer.padding == 5

    def test_render_double_bond(self) -> None:
        """Test rendering molecule with double bond."""
        mol = parse_smiles(ETHENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        # Double bond should use = character
        assert "=" in result

    def test_render_triple_bond(self) -> None:
        """Test rendering molecule with triple bond."""
        mol = parse_smiles(ETHYNE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = AsciiRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        # Triple bond should use # character
        assert "#" in result

    def test_bond_char_horizontal(self) -> None:
        """Test horizontal bond character selection."""
        renderer = AsciiRenderer()
        char = renderer._get_bond_char(0.0, 1)
        assert char == "-"

    def test_bond_char_vertical(self) -> None:
        """Test vertical bond character selection."""
        renderer = AsciiRenderer()
        char = renderer._get_bond_char(math.pi / 2, 1)
        assert char == "|"

    def test_bond_char_double(self) -> None:
        """Test double bond character selection."""
        renderer = AsciiRenderer()
        char = renderer._get_bond_char(0.0, 2)
        assert char == "="

    def test_bond_char_triple(self) -> None:
        """Test triple bond character selection."""
        renderer = AsciiRenderer()
        char = renderer._get_bond_char(0.0, 3)
        assert char == "#"

    def test_bond_char_diagonal(self) -> None:
        """Test diagonal bond character selection."""
        renderer = AsciiRenderer()
        char_up = renderer._get_bond_char(math.pi / 4, 1)
        char_down = renderer._get_bond_char(3 * math.pi / 4, 1)
        assert char_up in ["/", "\\"]
        assert char_down in ["/", "\\"]

    def test_output_fits_dimensions(self) -> None:
        """Test that output fits within specified dimensions."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        width, height = 40, 20
        renderer = AsciiRenderer(width=width, height=height)
        result = renderer.render(positions, bonds, symbols)

        lines = result.split("\n")
        assert len(lines) <= height
        for line in lines:
            assert len(line) <= width

    def test_transform_single_point(self) -> None:
        """Test transformation of single point."""
        renderer = AsciiRenderer(width=40, height=20)
        transform = renderer._compute_transform([(0.0, 0.0)])
        assert len(transform) == 4


class TestUnicodeRenderer:
    """Tests for Unicode rendering."""

    def test_render_empty_positions(self) -> None:
        """Test rendering with empty positions."""
        renderer = UnicodeRenderer()
        result = renderer.render([], [], [])
        assert result == ""

    def test_render_single_atom(self) -> None:
        """Test rendering a single atom."""
        renderer = UnicodeRenderer(width=20, height=10)
        result = renderer.render([(0.0, 0.0)], [], ["C"])
        assert "C" in result

    def test_render_returns_string(self) -> None:
        """Test that render returns a string."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert isinstance(result, str)

    def test_render_contains_atoms(self) -> None:
        """Test that rendered output contains atom symbols."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        assert "O" in result

    def test_render_benzene(self) -> None:
        """Test rendering benzene ring."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_molecule_method(self) -> None:
        """Test render_molecule convenience method."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render_molecule(mol)
        assert isinstance(result, str)
        assert "C" in result
        assert "O" in result

    def test_custom_dimensions(self) -> None:
        """Test renderer with custom dimensions."""
        renderer = UnicodeRenderer(width=100, height=50, padding=5)
        assert renderer.width == 100
        assert renderer.height == 50
        assert renderer.padding == 5

    def test_render_double_bond(self) -> None:
        """Test rendering molecule with double bond."""
        mol = parse_smiles(ETHENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        # Double bond should use ═ character
        assert "═" in result

    def test_render_triple_bond(self) -> None:
        """Test rendering molecule with triple bond."""
        mol = parse_smiles(ETHYNE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        renderer = UnicodeRenderer(width=40, height=20)
        result = renderer.render(positions, bonds, symbols)
        assert "C" in result
        # Triple bond should use ≡ character
        assert "≡" in result

    def test_bond_char_horizontal(self) -> None:
        """Test horizontal bond character selection."""
        renderer = UnicodeRenderer()
        char = renderer._get_bond_char(0.0, 1)
        assert char == "─"

    def test_bond_char_vertical(self) -> None:
        """Test vertical bond character selection."""
        renderer = UnicodeRenderer()
        char = renderer._get_bond_char(math.pi / 2, 1)
        assert char == "│"

    def test_bond_char_double_horizontal(self) -> None:
        """Test double horizontal bond character selection."""
        renderer = UnicodeRenderer()
        char = renderer._get_bond_char(0.0, 2)
        assert char == "═"

    def test_bond_char_double_vertical(self) -> None:
        """Test double vertical bond character selection."""
        renderer = UnicodeRenderer()
        char = renderer._get_bond_char(math.pi / 2, 2)
        assert char == "║"

    def test_bond_char_triple(self) -> None:
        """Test triple bond character selection."""
        renderer = UnicodeRenderer()
        char = renderer._get_bond_char(0.0, 3)
        assert char == "≡"

    def test_bond_char_diagonal(self) -> None:
        """Test diagonal bond character selection."""
        renderer = UnicodeRenderer()
        char_up = renderer._get_bond_char(math.pi / 4, 1)
        char_down = renderer._get_bond_char(3 * math.pi / 4, 1)
        assert char_up in ["╱", "╲"]
        assert char_down in ["╱", "╲"]

    def test_output_fits_dimensions(self) -> None:
        """Test that output fits within specified dimensions."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        symbols = atom_layout.get_symbols()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()

        width, height = 40, 20
        renderer = UnicodeRenderer(width=width, height=height)
        result = renderer.render(positions, bonds, symbols)

        lines = result.split("\n")
        assert len(lines) <= height
        for line in lines:
            assert len(line) <= width

    def test_transform_single_point(self) -> None:
        """Test transformation of single point."""
        renderer = UnicodeRenderer(width=40, height=20)
        transform = renderer._compute_transform([(0.0, 0.0)])
        assert len(transform) == 4
