# Bot Meta-Repository

A unified AI-powered assistant for document conversion, automated testing, and artifact generation - designed for business analysts and non-technical users.

## What This Does

This bot helps you:

- **Convert Documents** - Turn PDFs, Word, Excel, and more into LLM-friendly markdown
- **Generate Artifacts** - Create user stories, reports, and data exports from your documents
- **Automate Testing** - Create and maintain end-to-end tests that fix themselves
- **Track Changes** - Save versions of your work without knowing Git commands

**Everything works through plain English commands** - no technical knowledge required.

---

## Quick Start

### Step 1: Open in Cursor

Open this `bot` folder in Cursor editor.

### Step 2: Run Setup

In the Cursor chat, type:
```
setup
```

The AI assistant will guide you through:
- Installing required software
- Configuring your API key
- Setting up SharePoint integration
- Running verification tests

### Step 3: Start Using

Once setup is complete, just tell the assistant what you need:

- "Convert my files"
- "Create a user story"
- "Generate a test"
- "Help"

---

## How Commands Work

This bot uses Cursor's command system. When you type something like "setup" or "convert my files", here's what happens:

### Command Resolution

1. **Cursor looks for commands** in `.cursor/commands/` at the workspace root (`bot/.cursor/commands/`)
2. **Matches trigger phrases** - Each command file lists phrases that activate it (like "setup", "get started", "install")
3. **Executes the command** - The AI follows the instructions in the matched command file

### Command Structure

All commands are stored in `bot/.cursor/commands/`:
- **Meta-level commands** (setup, help, git) are directly in `commands/`
- **Domain-specific commands** are in subfolders:
  - `markitdown/` - Document conversion commands
  - `playwright/` - Testing commands

### Why This Matters

- **No ambiguity** - Each command has clear trigger phrases
- **Consistent experience** - Commands work the same way every time
- **Easy to extend** - New commands can be added by creating new `.md` files

**Note:** Old command files from the original repositories have been archived to prevent conflicts. The unified structure at `bot/.cursor/` is the single source of truth.

---

## Available Commands

### Document Conversion

| Say This | What Happens |
|----------|--------------|
| "Convert my files" | Converts documents from SharePoint folders to markdown |
| "Convert report.pdf" | Converts a specific file (finds it in SharePoint folders) |
| "Sync my files" | Shows conversion status |
| "Sync references" | Updates markdown from SharePoint (full sync) |

**Supported files:** PDF, Word, Excel, PowerPoint, images, text, HTML

Files are converted from your SharePoint folders into reference markdown folders (`*_reference_md/`).

### SharePoint Integration

| Say This | What Happens |
|----------|--------------|
| "Sync references" | Updates markdown from SharePoint folders |

The bot reads your SharePoint folders and creates markdown versions for AI processing.

### Artifact Generation

| Say This | What Happens |
|----------|--------------|
| "Create artifact" | Generate user stories, reports, exports |
| "Create user story" | Generate a specific type |

### Automated Testing

| Say This | What Happens |
|----------|--------------|
| "Generate test" | Create new E2E test |
| "Run all tests" | Execute test suite |
| "Run test headed" | Watch test execute |
| "Analyze results" | Understand failures |

### Version Control

| Say This | What Happens |
|----------|--------------|
| "Save my work" | Create a checkpoint |
| "Show history" | View past saves |
| "Undo changes" | Restore previous version |
| "Backup" | Upload to GitHub |

### Help

| Say This | What Happens |
|----------|--------------|
| "Help" | Show all commands |
| "Help with converting" | Topic-specific help |

---

## Folder Structure

When deployed to SharePoint:

```
sharepoint/
├── [your_folders]/           # Original documents (READ-ONLY)
├── [folder]_reference_md/    # Generated markdown references
├── unfiled_reference_md/     # References for root files
├── artifacts/                # Generated artifacts
│   ├── user_stories/
│   ├── reports/
│   └── exports/
└── bot/                      # This repository
    ├── ba_markitdown/        # Document conversion tools
    ├── cursor-playwright/    # Testing tools
    ├── config/               # Configuration files
    └── .env                  # Your credentials (private!)
```

---

## Important Security Notes

### API Keys

**NEVER paste API keys in the chat!**

When setting up your API key:
1. Open the `.env` file directly
2. Paste your key there
3. Save the file

If you accidentally paste a key in chat:
1. Go to your API provider immediately
2. Revoke the exposed key
3. Generate a new one

### Protected Folders

Original SharePoint folders are **read-only** through this bot. The bot will:
- ✓ Read files for conversion
- ✓ Create markdown references
- ✓ Generate artifacts
- ✗ Never modify original files

---

## Troubleshooting

### "Setup didn't complete"

Run `setup` again. The assistant will detect what's missing.

### "API key not working"

1. Open `.env` file
2. Check `API_KEY` is filled in correctly
3. Verify key is active at your provider's dashboard

### "Tests are failing"

1. Run "run test headed" to watch what's happening
2. If feature works manually → "Self-Heal [Test Name]"
3. If feature is broken → Report to development team

### "Can't convert file"

- Check file is in one of your SharePoint folders (at the same level as bot/)
- Run "sync references" to check if file needs conversion
- Audio/video files need ffmpeg installed
- Password-protected files need to be unlocked first

---

## For Technical Users

<details>
<summary>Click to expand technical details</summary>

### Manual Commands

**Document conversion:**
```bash
cd ba_markitdown
uv run python main.py input.pdf output.md --cleanup --frontmatter
```

**Run tests:**
```bash
cd cursor-playwright
npx playwright test
npx playwright test --headed
```

### Environment Variables

`.env` file:
```
# LLM Configuration
API_KEY=your_google_api_key
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.0-flash

# Testing Configuration
APP_URL=https://your-app.com
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=your_password
```

### Configuration Files

- `config/setup_status.json` - Installation state
- `config/categories.json` - Artifact category mappings
- `config/protected_paths.json` - Read-only folder list

### Command System Architecture

- **Unified commands**: `bot/.cursor/commands/` - All commands are here
- **Archived commands**: `ba_markitdown/.cursor_old/` and `cursor-playwright/.cursor_old/` - Old commands preserved but inactive
- **Command resolution**: Cursor searches `bot/.cursor/commands/` first, ensuring unified commands take precedence

### Installation Modes

- **venv** - Full installation with virtual environment
- **ephemeral** - Dependencies loaded on-demand (for restricted environments)

The system auto-detects and uses the best mode for your environment.

</details>

---

## Getting Help

Just say "help" in the Cursor chat anytime!

For specific topics:
- "Help with converting"
- "Help with testing"
- "Help with artifacts"
- "Help with saving"

---

## Version

Bot Meta-Repository v1.0.0

Components:
- BA MarkItDown (document conversion)
- Cursor Playwright (automated testing)
- SharePoint Integration
- Artifact Generation
