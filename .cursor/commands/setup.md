---
name: Setup
description: Initialize and configure the Bot Meta-Repository with all required dependencies
---

# Bot Meta-Repository Setup

This command guides users through complete setup of the bot system, including:
- Environment detection and dependency installation
- Git initialization
- Environment file configuration
- Verification tests
- SharePoint folder scanning and reference generation
- Artifact category configuration

## Trigger Phrases

Activate when user says:
- "Setup"
- "Get started"
- "Install"
- "Initialize"
- "Configure"
- "First time setup"
- "Set up my environment"

## Instructions for Cursor

This is a multi-phase setup workflow. Follow each phase completely before moving to the next.

═══════════════════════════════════════════════════════════════
PHASE 1: ENVIRONMENT DETECTION
═══════════════════════════════════════════════════════════════

### Step 1.1: Welcome and Check Environment

Display:
```
═══════════════════════════════════════════════════════════════
       WELCOME TO BOT SETUP
═══════════════════════════════════════════════════════════════

I'm going to set up everything you need. This includes:
✓ Installing required software packages
✓ Setting up your configuration
✓ Preparing the SharePoint connection
✓ Running verification tests

Let me check your system first...
```

Run environment check:
```bash
python setup.py --json
```

Parse the JSON output and present results:
```
System Check Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Show each check result with friendly icons]
✓ Python [version] - Ready
✓ Node.js [version] - Ready (or ✗ Not found)
✓ uv package manager - Available (or - Not found, using alternative)
✓ Git - Available

Recommended installation mode: [venv/ephemeral]
```

### Step 1.2: Handle Missing Node.js

If Node.js is not found:
```
Node.js is required for the automated testing features. 

To install Node.js:
1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer and follow the prompts
4. Restart this terminal after installation

Would you like me to:
a) Continue without testing features (you can add them later)
b) Wait while you install Node.js

Just let me know when you're ready to continue.
```

Wait for user response. If they choose to continue without Node:
- Note in setup_status.json that playwright features are disabled
- Skip Node-related installation steps

═══════════════════════════════════════════════════════════════
PHASE 2: DEPENDENCY INSTALLATION
═══════════════════════════════════════════════════════════════

### Step 2.1: Install Python Dependencies

Display:
```
Installing Python packages...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Based on recommended_mode from check:

**If mode is "venv" or "venv_pip":**
```bash
cd ba_markitdown && uv sync
```
Or if using pip:
```bash
cd ba_markitdown && python -m venv .venv && .venv/Scripts/pip install -e .
```

**If installation fails:**
```
Installation couldn't complete normally, but don't worry!
I'll use on-demand mode instead - everything will still work,
it just loads fresh each time you use it.
```
Set install_mode to "ephemeral" in config/setup_status.json

**If successful:**
```
✓ Python packages installed successfully!
```

### Step 2.2: Install Node.js Dependencies (if Node available)

Display:
```
Installing Node.js packages...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
cd cursor-playwright && npm install
```

**If fails:**
```
Node.js packages couldn't be installed.
Testing features will use on-demand mode.
```

**If successful:**
```
✓ Node.js packages installed!
```

### Step 2.3: Install Playwright Browsers (if Node available)

Display:
```
Setting up browser for automated testing...
(This may take a minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
cd cursor-playwright && npx playwright install chromium
```

**If successful:**
```
✓ Browser installed and ready!
```

═══════════════════════════════════════════════════════════════
PHASE 3: GIT INITIALIZATION
═══════════════════════════════════════════════════════════════

### Step 3.1: Backup Existing Git (if needed)

Check for existing git in sub-repos:
```bash
python setup.py --backup-git --json
```

If backups were created:
```
I found existing version history in the sub-projects.
I've backed these up safely in case you need them later.
```

### Step 3.2: Initialize Fresh Git

```bash
python setup.py --init-git --json
```

Display:
```
✓ Version control initialized!
  Your work will now be tracked and you can save checkpoints.
```

═══════════════════════════════════════════════════════════════
PHASE 4: ENVIRONMENT CONFIGURATION
═══════════════════════════════════════════════════════════════

### Step 4.1: Create .env File (ADDITIVE ONLY)

Check if .env exists:
```bash
test -f .env && echo "exists" || echo "not found"
```

**CRITICAL - ADDITIVE OPERATIONS ONLY:**

**If .env does NOT exist:**
- Create from template:
  ```bash
  cp .env.example .env
  ```
- Inform user: "Created .env from template. All values are placeholders - you need to fill them in."

**If .env EXISTS:**
- **DO NOT overwrite or modify existing .env**
- Read current .env to check what's configured
- Inform user:
  ```
  .env file already exists with your configuration.
  
  Current configuration:
  - MarkItDown: [configured/not configured]
  - Playwright: [configured/not configured]
  
  If you need to add missing values, I can help you add them
  without overwriting your existing settings.
  
  Would you like to:
  a) Keep current .env and add any missing values
  b) Review current .env file
  c) Skip .env configuration
  ```
- Only add missing variables if user requests, preserving all existing values

**NEVER:**
- Overwrite existing .env with `cp .env.example .env`
- Remove or change existing values without explicit user request
- Use destructive file operations on .env

### Step 4.2: Prompt User for Configuration

**CRITICAL - READ THIS CAREFULLY:**

Display:
```
═══════════════════════════════════════════════════════════════
IMPORTANT: Configure Your Credentials
═══════════════════════════════════════════════════════════════

I've created a configuration file at: .env

You need to add your credentials to this file.

⚠️  SECURITY WARNING ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DO NOT paste your API key or passwords in this chat!
That would send them through external services and compromise
your security.

Instead, please:
1. Open the .env file directly in your editor
2. Fill in your values:
   - API_KEY: Get from https://aistudio.google.com/apikey
   - LLM_MODEL: Use "gemini-2.0-flash" (recommended)
   - APP_URL: The URL of your test application (if using tests)
   - TEST_USER credentials (if using tests)
3. Save the file

When you're done, just say "done" or "continue" and I'll verify 
your configuration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**WAIT for user to confirm they've updated the file.**

Do NOT proceed until user says something like:
- "done"
- "continue"
- "ready"
- "finished"
- "I've updated it"

═══════════════════════════════════════════════════════════════
PHASE 5: VERIFICATION TESTS
═══════════════════════════════════════════════════════════════

After user confirms .env is configured:

### Step 5.1: Verify Configuration

Display:
```
Verifying your configuration...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Read config/setup_status.json to get install_mode.

### Step 5.2: Test Markitdown Conversion

**If install_mode is "venv":**
```bash
cd ba_markitdown && python test_files/../verify_markitdown.py
```

**If install_mode is "ephemeral":**
```bash
cd ba_markitdown && uv run python ../test_files/verify_markitdown.py
```

Report result:
- ✓ Document conversion is working!
- ✗ Document conversion test failed. [Show error and guidance]

### Step 5.3: Test API Connection

Run API verification:
```bash
python test_files/verify_api.py
```
Or in ephemeral mode:
```bash
uv run python test_files/verify_api.py
```

Report result:
- ✓ API connection successful!
- ✗ Couldn't connect to API. Please check your API_KEY in .env

### Step 5.4: Test Playwright (if Node available)

```bash
cd cursor-playwright && npx playwright test --list
```

Report result:
- ✓ Playwright is ready!
- ✗ Playwright test failed. [Show error]

### Step 5.5: Verification Summary

Display:
```
═══════════════════════════════════════════════════════════════
VERIFICATION RESULTS
═══════════════════════════════════════════════════════════════

✓ Document Conversion: Working
✓ API Connection: Connected
✓ Playwright: Ready (or ⊘ Skipped)

[If any failed, show troubleshooting steps]
```

Update config/setup_status.json with verification results:
```bash
python -c "
import json
from datetime import datetime
with open('config/setup_status.json', 'r') as f:
    status = json.load(f)
status['verification'] = {
    'markitdown_test': 'passed',
    'playwright_test': 'passed',
    'api_test': 'passed',
    'last_verified': datetime.now().isoformat()
}
status['env_configured'] = True
with open('config/setup_status.json', 'w') as f:
    json.dump(status, f, indent=2)
"
```

═══════════════════════════════════════════════════════════════
PHASE 6: SHAREPOINT CONFIGURATION
═══════════════════════════════════════════════════════════════

### Step 6.1: Scan SharePoint Structure

```bash
python setup.py --scan-sharepoint --json
```

Display:
```
Scanning SharePoint folder structure...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I found the following folders in your SharePoint:

📁 [folder1_name] - [X] files
📁 [folder2_name] - [Y] files
📄 [Z] files at root level

These folders contain your source documents. I'll create 
reference markdown versions that can be used for generating
artifacts.
```

### Step 6.2.1: Create Technical Protection (.cursorignore)

Create a .cursorignore file at the workspace root to block all write operations to SharePoint folders:

```bash
python setup.py --create-cursorignore --json
```

Parse the JSON output. If successful, display:

```
Creating technical protection for SharePoint folders...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm setting up protection so that your original SharePoint
documents cannot be accidentally modified through this bot.

Protected folders:
- [folder1]
- [folder2]
- ...

These folders are now READ-ONLY through Cursor.
```

**If this fails:**
- Show error message
- Continue with setup (protection will be incomplete but setup can proceed)

### Step 6.2.2: Create Reference and Artifacts Folders

For each SharePoint folder, create a corresponding reference markdown folder.
Also create the artifacts folder with subfolders.

```bash
python setup.py --create-folders --json
```

Parse the JSON output. If successful, display:

```
Creating output folders...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created reference folders:
✓ folder1_reference_md/
✓ folder2_reference_md/
✓ unfiled_reference_md/

Created artifacts folders:
✓ artifacts/user_stories/
✓ artifacts/reports/
✓ artifacts/exports/
✓ artifacts/images/
```

**If this fails:**
- Show error message
- Continue with setup (folders can be created manually later)

### Step 6.3: Save Protected Paths

Update config/protected_paths.json with the original SharePoint folders from scan results:

```bash
cd unified-bot && python -c "
from setup import scan_sharepoint_structure, save_protected_paths
scan_result = scan_sharepoint_structure()
folder_names = [f['name'] for f in scan_result.get('folders', [])]
save_protected_paths(folder_names)
print('Protected paths saved')
"
```

Display:
```
Saved protected folder list to config/protected_paths.json

[Show list of protected folders]
```

### Step 6.4: Generate Initial Reference Markdown

Display:
```
Generating reference markdown files from your documents...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This converts your documents to a format that's easy for me
to read and use when generating artifacts.

Processing [folder1]... [X/Y files]
Processing [folder2]... [X/Y files]
Processing root files... [X/Y files]
```

For each file, use markitdown to convert (respecting install_mode):

**venv mode:**
```bash
python ba_markitdown/main.py "../folder1/document.pdf" "../folder1_reference_md/document.md" --frontmatter --cleanup
```

**ephemeral mode:**
```bash
uv run python ba_markitdown/main.py "../folder1/document.pdf" "../folder1_reference_md/document.md" --frontmatter --cleanup
```

═══════════════════════════════════════════════════════════════
PHASE 7: ARTIFACT CATEGORIES
═══════════════════════════════════════════════════════════════

### Step 7.1: Present Default Categories

Display:
```
Setting up artifact categories...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Artifacts are the documents and files I can generate for you
based on your SharePoint content.

I've set up these default categories:

1. user_stories - For user story documents
2. images - For generated images and diagrams  
3. reports - For generated reports and summaries
4. exports - For exported data files

Would you like to add any additional categories?
(Just say "no" to keep the defaults, or tell me what categories 
you'd like to add)
```

### Step 7.2: Handle Custom Categories

If user wants to add categories:
```
What would you like to call this category?
```

Wait for response, then:
```
What kind of files should this category produce?
(e.g., markdown, excel, csv, images)
```

Add to config/categories.json

### Step 7.3: Map Categories to Reference Folders

For each category:
```
Which reference folders should "[category]" use for information?

Available folders:
1. folder1_reference_md
2. folder2_reference_md
3. unfiled_reference_md (automatically included for all)

Enter the numbers separated by commas, or say "all":
```

Update config/categories.json with the mappings.

═══════════════════════════════════════════════════════════════
PHASE 8: COMPLETION
═══════════════════════════════════════════════════════════════

Update setup_status.json:
```bash
python -c "
import json
from datetime import datetime
with open('config/setup_status.json', 'r') as f:
    status = json.load(f)
status['setup_complete'] = True
status['sharepoint_configured'] = True
status['categories_configured'] = True
status['last_setup'] = datetime.now().isoformat()
with open('config/setup_status.json', 'w') as f:
    json.dump(status, f, indent=2)
"
```

Display final message:
```
═══════════════════════════════════════════════════════════════
       SETUP COMPLETE! 🎉
═══════════════════════════════════════════════════════════════

Everything is configured and ready to use!

Here's what you can do now:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 DOCUMENT CONVERSION
   Say "convert my files" to convert documents to markdown
   
🔄 REFERENCE SYNC
   Say "sync references" to update markdown from SharePoint
   
📝 ARTIFACTS
   Say "create artifact" to generate user stories, reports, etc.
   
🧪 TESTING (if configured)
   Say "generate test" to create automated tests
   Say "run all tests" to check your application
   
💾 VERSION CONTROL
   Say "save my work" to create a checkpoint
   Say "show history" to see past saves
   
❓ HELP
   Say "help" anytime to see all available commands

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What would you like to do first?
═══════════════════════════════════════════════════════════════
```

═══════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════

### If Python installation fails completely:
```
I couldn't install the Python packages, but I can still help!
I'll load what's needed each time you run a command.
This is called "ephemeral mode" - it works just as well,
just takes a moment longer each time.
```
Continue with ephemeral mode.

### If user pastes an API key in chat:
**IMMEDIATELY** display security warning per security.mdc rules.
Do not continue until user confirms they've regenerated the key.

### If verification tests fail:
```
Some tests didn't pass. Let's troubleshoot:

[For API test failure]
- Check that your API_KEY is correct in .env
- Make sure you copied the full key (it's usually quite long)
- Verify your API key is active at https://aistudio.google.com/apikey

[For Playwright failure]
- This might be a browser installation issue
- Try running: npx playwright install chromium

Would you like to:
a) Try the failing tests again
b) Continue anyway and fix later
c) Get more detailed error information
```

### If SharePoint folder is empty:
```
I don't see any folders in your SharePoint location yet.
That's okay! You can add folders later and run "sync references"
to update.
```
