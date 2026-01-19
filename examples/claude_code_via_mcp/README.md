# chemscii Claude Code Integration via MCP

This example demonstrates how to integrate chemscii with [Claude Code](https://github.com/anthropics/claude-code) using the Model Context Protocol (MCP).

## How It Works

Claude Code supports MCP servers that provide tools Claude can use directly. The chemscii MCP server exposes a `render_molecule` tool that Claude can call to render chemical structures without needing CLI instructions.

Unlike the CLAUDE.md approach, MCP integration:
- Works globally (not directory-scoped)
- Provides a structured tool interface
- Gives Claude direct access to rendering parameters

## Setup

1. Install chemscii:
   ```bash
   pip install chemscii
   ```

2. Add the MCP server to your Claude Code settings. Edit `~/.claude.json`:
   ```json
   "mcpServers": {
     "chemscii": {
       "command": "chemscii",
       "type": "stdio",
       "args": [
         "--mcp"
       ]
     }
   }
   ```

3. Restart Claude Code to load the MCP server. Check with `claude mcp list`

## Example Usage

Once configured, Claude Code has access to the `render_molecule` tool. Try these prompts:

### Basic Rendering
> "Show me caffeine"

> "What does aspirin look like?"

> "Render the molecule that gives bananas their smell"

### Renderer Options
> "Show me cholesterol using the unicode renderer"

> "Render dopamine with ascii art"

### Chemistry Questions
> "What's the structure of the active ingredient in coffee?"

> "Show me the difference between glucose and fructose"

### Using SMILES Notation
> "Render this SMILES: c1ccc2c(c1)cc1ccccc1n2"

## Tool Parameters

The `render_molecule` tool accepts these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `molecule` | string | required | SMILES string, molecule name, ChEMBL ID, or SDF content |
| `renderer` | string | "magic" | Renderer type: "ascii", "unicode", or "magic" |
| `width` | int | 60 | Canvas width for ascii/unicode renderers |
| `height` | int | 30 | Canvas height for ascii/unicode renderers |
| `columns` | int | 80 | Output width for magic renderer |
| `escape_codes` | bool | false | Include escape codes for color rendering |

## How This Differs from Other Integrations

| Approach | Setup Required | Works With | Scope |
|----------|---------------|------------|-------|
| CLAUDE.md | None | Claude Code | Directory-scoped |
| **MCP Server (this)** | JSON config editing | Claude Code, Claude Desktop | Global |
| API Script | API key + environment | Any Python environment | Programmatic |

## Advantages of MCP

- **Global availability**: Works in any directory once configured
- **Structured interface**: Claude receives typed parameters and documentation
- **Works with Claude Desktop**: Can also be used with Claude Desktop app
- **Explicit tool calls**: You can see when Claude uses the tool in the conversation

## Limitations

- **Requires configuration**: Must edit settings.json to enable
- **Server process**: Runs as a subprocess managed by Claude Code
- **Single instance**: One server configuration per settings file
