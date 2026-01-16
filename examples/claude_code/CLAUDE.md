# chemscii Claude Code Integration

When users ask about chemical structures, molecules, or compounds, render them using the `chemscii` CLI.

## Default Rendering

Use the magic renderer (default) with 50 columns:

```bash
chemscii "<molecule>"
```

Examples:
- `chemscii "caffeine"` - render by common name
- `chemscii "aspirin"` - render by drug name
- `chemscii "CCO"` - render by SMILES notation
- `chemscii "CHEMBL25"` - render by ChEMBL ID

## Larger Renderings

If users ask for a larger, bigger, or more detailed rendering, increase columns to 100:

```bash
chemscii "<molecule>" --columns 100
```

## Alternative View

If users ask for a different view, alternative rendering, or simpler output, use the Unicode renderer:

```bash
chemscii "<molecule>" --unicode --width 80 --height 40
```

For an even simpler ASCII-only view:

```bash
chemscii "<molecule>" --ascii --width 80 --height 40
```

## Responding to Users

After rendering a molecule:
1. Display the rendered output
2. Briefly explain what the molecule is and its significance
3. Mention any interesting structural features visible in the rendering

## Input Detection

The CLI automatically detects input type:
- Common names: caffeine, aspirin, glucose, cholesterol
- SMILES strings: CCO, c1ccccc1, CC(=O)Oc1ccccc1C(=O)O
- ChEMBL IDs: CHEMBL25, CHEMBL113
- File paths: molecule.sdf, structure.mol
