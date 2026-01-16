# chemscii Claude Code Integration

This example demonstrates how to integrate chemscii with [Claude Code](https://github.com/anthropics/claude-code) using a simple CLAUDE.md instruction file.

## How It Works

Claude Code automatically reads `CLAUDE.md` files in your project directory. These files provide context and instructions that guide Claude's behavior when working in that directory.

The `CLAUDE.md` in this example teaches Claude how to use the chemscii CLI to render chemical structures when users ask about molecules. No API keys, configuration files, or additional setup required.

## Setup

1. Install chemscii:
   ```bash
   pip install chemscii
   ```

2. Navigate to this directory (or copy `CLAUDE.md` to your project):
   ```bash
   cd examples/claude_code
   ```

3. Start Claude Code:
   ```bash
   claude
   ```

## Example Usage

Once Claude Code is running in this directory, try these prompts:

### Basic Rendering
> "Show me caffeine"

> "What does aspirin look like?"

> "Render the molecule that gives bananas their smell"

### Larger Output
> "Show me cholesterol, make it bigger"

> "Render dopamine with more detail"

### Alternative Views
> "Show me benzene in a different style"

> "Render ethanol using Unicode characters"

### Chemistry Questions
> "What's the structure of the active ingredient in coffee?"

> "Show me the difference between glucose and fructose"

### Using SMILES Notation
> "Render this SMILES: c1ccc2c(c1)cc1ccccc1n2"

## Customization

Edit `CLAUDE.md` to adjust the default behavior:

- Change default column width
- Add domain-specific molecule aliases
- Customize the explanation style
- Add project-specific rendering preferences

## How This Differs from Other Integrations

| Approach | Setup Required | Works With |
|----------|---------------|------------|
| **CLAUDE.md (this)** | None | Claude Code |
| MCP Server | JSON config editing | Claude Code, Claude Desktop |
| API Script | API key + environment setup | Any Python environment |

The CLAUDE.md approach is the simplest: anyone who clones this repo and has chemscii installed can immediately use the integration with zero configuration.

### Limitations of the CLAUDE.md Approach

- **Claude Code only**: Does not work with Claude Desktop, the web interface, or API integrations
- **Directory-scoped**: Instructions only apply when Claude Code is running in this directory (or a subdirectory)
- **Guidance, not guarantees**: CLAUDE.md provides instructions that Claude follows, but it uses judgment in interpretation. Results may vary slightly between sessions
- **CLI-dependent**: Requires the chemscii CLI to be installed and accessible in the shell
- **No programmatic integration**: Cannot be embedded in scripts, pipelines, or automated workflows
- **Limited to CLI capabilities**: Cannot add custom logic beyond what the chemscii CLI provides
