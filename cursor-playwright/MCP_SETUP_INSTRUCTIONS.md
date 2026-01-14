# Playwright MCP Server Setup Instructions

To enable the Playwright MCP server for test generation, you need to configure it in Cursor's settings:

## Setup Steps:

1. Open Cursor Settings (Ctrl+, or Cmd+,)
2. Search for "MCP" or navigate to "Features" > "MCP"
3. Click "Edit Config" or add the following configuration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"],
      "capabilities": ["testing"]
    }
  }
}
```

4. Save the configuration file
5. Restart Cursor to load the MCP server

## Verification:

After restarting Cursor, you should see the Playwright MCP server listed in your available MCP servers. The `testing` capability enables the `browser_generate_locator` tool which is used for creating robust Playwright test locators.

## What This Enables:

- **browser_generate_locator**: Generates Playwright locators from browser plugin element references
- Integration between the browser plugin and Playwright test code generation

## Troubleshooting:

If the server doesn't appear after restart:
1. Ensure you have internet connectivity (to download @playwright/mcp)
2. Check that npx is available in your PATH
3. Look at Cursor's MCP logs for any error messages
