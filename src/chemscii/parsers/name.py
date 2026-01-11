"""Convert molecule names to SMILES strings."""

from __future__ import annotations

from urllib import error, parse, request

# Common molecule names for quick local lookup
_COMMON_MOLECULES: dict[str, str] = {
    "water": "O",
    "methane": "C",
    "ethane": "CC",
    "propane": "CCC",
    "butane": "CCCC",
    "methanol": "CO",
    "ethanol": "CCO",
    "propanol": "CCCO",
    "acetone": "CC(=O)C",
    "benzene": "c1ccccc1",
    "toluene": "Cc1ccccc1",
    "phenol": "Oc1ccccc1",
    "acetic acid": "CC(=O)O",
    "formic acid": "C(=O)O",
    "ammonia": "N",
    "carbon dioxide": "O=C=O",
    "aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    "glucose": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
}


def name_to_smiles(name: str, use_pubchem: bool = True) -> str | None:
    """Convert a molecule name to its SMILES representation.

    First checks a local dictionary of common molecules, then optionally
    queries PubChem for unknown names.

    Args:
        name: The common or IUPAC name of a molecule.
        use_pubchem: Whether to query PubChem for unknown names.

    Returns:
        The SMILES string if found, None otherwise.
    """
    if not name or not name.strip():
        return None

    normalized = name.lower().strip()

    # Check local dictionary first
    if normalized in _COMMON_MOLECULES:
        return _COMMON_MOLECULES[normalized]

    # Query PubChem if enabled
    if use_pubchem:
        return _query_pubchem(name)

    return None


def _query_pubchem(name: str) -> str | None:
    """Query PubChem for a molecule's SMILES by name.

    Args:
        name: The molecule name to search for.

    Returns:
        The canonical SMILES if found, None otherwise.
    """
    encoded_name = parse.quote(name)
    url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{encoded_name}/property/CanonicalSMILES/TXT"
    )

    try:
        with request.urlopen(url, timeout=10) as response:
            smiles = response.read().decode("utf-8").strip()
            return smiles if smiles else None
    except (error.URLError, error.HTTPError, TimeoutError):
        return None
