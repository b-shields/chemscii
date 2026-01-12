"""Tests for chemscii.layout module."""

from chemscii.layout.atoms import AtomLayout
from chemscii.layout.bonds import BondLayout
from chemscii.parsers.molecule import parse_smiles
from tests.fixtures.molecules import BENZENE, ETHANOL, ETHENE, ETHYNE, METHANE


class TestAtomLayout:
    """Tests for atom positioning."""

    def test_compute_positions_ethanol(self) -> None:
        """Test computing positions for ethanol."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        positions = layout.compute_positions()
        assert len(positions) == 3  # C, C, O

    def test_compute_positions_benzene(self) -> None:
        """Test computing positions for benzene."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        layout = AtomLayout(mol)
        positions = layout.compute_positions()
        assert len(positions) == 6  # 6 carbons

    def test_compute_positions_single_atom(self) -> None:
        """Test computing positions for single atom."""
        mol = parse_smiles(METHANE)
        assert mol is not None
        layout = AtomLayout(mol)
        positions = layout.compute_positions()
        assert len(positions) == 1

    def test_positions_are_tuples(self) -> None:
        """Test that positions are (x, y) tuples."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        positions = layout.compute_positions()
        for pos in positions:
            assert isinstance(pos, tuple)
            assert len(pos) == 2
            assert isinstance(pos[0], float)
            assert isinstance(pos[1], float)

    def test_get_symbols(self) -> None:
        """Test getting atom symbols."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        layout.compute_positions()
        symbols = layout.get_symbols()
        assert len(symbols) == 3
        assert symbols.count("C") == 2
        assert symbols.count("O") == 1

    def test_get_bounds(self) -> None:
        """Test getting bounding box."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        layout.compute_positions()
        bounds = layout.get_bounds()
        assert len(bounds) == 4
        min_x, min_y, max_x, max_y = bounds
        assert max_x >= min_x
        assert max_y >= min_y

    def test_get_bounds_empty(self) -> None:
        """Test bounding box before compute_positions."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        bounds = layout.get_bounds()
        assert bounds == (0.0, 0.0, 0.0, 0.0)

    def test_positions_stored(self) -> None:
        """Test that positions are stored in instance."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        layout = AtomLayout(mol)
        positions = layout.compute_positions()
        assert layout.positions == positions


class TestBondLayout:
    """Tests for bond positioning."""

    def test_compute_bond_lines_ethanol(self) -> None:
        """Test computing bond lines for ethanol."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        assert len(bonds) == 2  # C-C and C-O

    def test_compute_bond_lines_benzene(self) -> None:
        """Test computing bond lines for benzene."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        assert len(bonds) == 6  # 6 bonds in ring

    def test_bond_line_format(self) -> None:
        """Test bond line tuple format."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        for bond in bonds:
            assert isinstance(bond, tuple)
            assert len(bond) == 3
            start, end, order = bond
            assert isinstance(start, tuple)
            assert isinstance(end, tuple)
            assert len(start) == 2
            assert len(end) == 2
            assert isinstance(order, int)

    def test_single_bond_order(self) -> None:
        """Test single bond has order 1."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        for _, _, order in bonds:
            assert order == 1

    def test_double_bond_order(self) -> None:
        """Test double bond has order 2."""
        mol = parse_smiles(ETHENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        assert len(bonds) == 1
        _, _, order = bonds[0]
        assert order == 2

    def test_triple_bond_order(self) -> None:
        """Test triple bond has order 3."""
        mol = parse_smiles(ETHYNE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        bonds = bond_layout.compute_bond_lines()
        assert len(bonds) == 1
        _, _, order = bonds[0]
        assert order == 3

    def test_get_aromatic_bonds(self) -> None:
        """Test detecting aromatic bonds."""
        mol = parse_smiles(BENZENE)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        aromatic = bond_layout.get_aromatic_bonds()
        assert len(aromatic) == 6  # All 6 bonds are aromatic

    def test_no_aromatic_bonds(self) -> None:
        """Test non-aromatic molecule has no aromatic bonds."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        atom_layout = AtomLayout(mol)
        positions = atom_layout.compute_positions()
        bond_layout = BondLayout(mol, positions)
        aromatic = bond_layout.get_aromatic_bonds()
        assert len(aromatic) == 0

    def test_empty_positions(self) -> None:
        """Test with empty positions list."""
        mol = parse_smiles(ETHANOL)
        assert mol is not None
        bond_layout = BondLayout(mol, [])
        bonds = bond_layout.compute_bond_lines()
        assert len(bonds) == 0
