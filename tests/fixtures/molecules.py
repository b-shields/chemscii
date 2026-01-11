"""Test fixtures for molecule SMILES and SDF data."""

# Simple molecules for basic testing
ETHANOL = "CCO"
METHANE = "C"
WATER = "O"
BENZENE = "c1ccccc1"
ACETIC_ACID = "CC(=O)O"

# Drug-like molecules
ASPIRIN = "CC(=O)OC1=CC=CC=C1C(=O)O"
CAFFEINE = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
IBUPROFEN = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"

# Molecules with different bond types
ETHENE = "C=C"  # Double bond
ETHYNE = "C#C"  # Triple bond
CYCLOHEXANE = "C1CCCCC1"  # Ring

# Test cases dict for parametrized testing
SMILES_TEST_CASES = {
    "ethanol": ETHANOL,
    "methane": METHANE,
    "water": WATER,
    "benzene": BENZENE,
    "acetic_acid": ACETIC_ACID,
    "aspirin": ASPIRIN,
    "caffeine": CAFFEINE,
    "ibuprofen": IBUPROFEN,
    "ethene": ETHENE,
    "ethyne": ETHYNE,
    "cyclohexane": CYCLOHEXANE,
}
