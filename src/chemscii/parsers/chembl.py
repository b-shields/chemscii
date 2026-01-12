"""Fetch SMILES from ChEMBL database by ID."""

from __future__ import annotations

import json
import re
from urllib import error, request

# Common ChEMBL IDs for quick local lookup (useful for testing)
_COMMON_CHEMBL: dict[str, str] = {
    "CHEMBL25": "CC(=O)Oc1ccccc1C(=O)O",  # Aspirin
    "CHEMBL113": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine
    "CHEMBL521": "CCO",  # Ethanol
    "CHEMBL545": "CO",  # Methanol
    "CHEMBL27732": "O",  # Water
    "CHEMBL1201320": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",  # Ibuprofen
}

# Pattern for valid ChEMBL IDs
_CHEMBL_PATTERN = re.compile(r"^CHEMBL\d+$", re.IGNORECASE)


def chembl_to_smiles(chembl_id: str, use_api: bool = True) -> str | None:
    """Fetch SMILES string for a ChEMBL compound ID.

    First checks a local cache of common compounds, then optionally
    queries the ChEMBL API for unknown IDs.

    Args:
        chembl_id: A ChEMBL compound identifier (e.g., 'CHEMBL25').
        use_api: Whether to query the ChEMBL API for unknown IDs.

    Returns:
        The SMILES string if found, None otherwise.
    """
    if not chembl_id or not chembl_id.strip():
        return None

    normalized = chembl_id.strip().upper()

    # Validate ChEMBL ID format
    if not _CHEMBL_PATTERN.match(normalized):
        return None

    # Check local cache first
    if normalized in _COMMON_CHEMBL:
        return _COMMON_CHEMBL[normalized]

    # Query ChEMBL API if enabled
    if use_api:
        return _query_chembl(normalized)

    return None


def _query_chembl(chembl_id: str) -> str | None:
    """Query ChEMBL API for a compound's SMILES.

    Args:
        chembl_id: The ChEMBL ID to look up (must be uppercase).

    Returns:
        The canonical SMILES if found, None otherwise.
    """
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"

    try:
        req = request.Request(url, headers={"Accept": "application/json"})
        with request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            structures = data.get("molecule_structures")
            if structures and isinstance(structures, dict):
                smiles = structures.get("canonical_smiles")
                if isinstance(smiles, str):
                    return smiles
            return None
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None
