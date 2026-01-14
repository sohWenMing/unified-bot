---
name: Create Artifact
description: Generate artifacts (user stories, reports, exports) from reference markdown files
---

# Create Artifact

This command generates artifacts such as user stories, reports, images, and data exports based on the reference markdown files converted from SharePoint documents.

## Trigger Phrases

Activate when user says:
- "Create artifact"
- "Generate artifact"
- "Create user story"
- "Generate user story"
- "Create report"
- "Generate report"
- "Export data"
- "Create export"
- "Make a [category]"

## Instructions for Cursor

═══════════════════════════════════════════════════════════════
PRE-CREATION CHECKS
═══════════════════════════════════════════════════════════════

### Step 1: Check Setup Status

Read config/setup_status.json:
```bash
cat config/setup_status.json
```

If `setup_complete` is false:
```
You haven't completed setup yet. Would you like to run setup first?
Say "setup" to get started.
```
STOP and wait for user.

### Step 2: Get Install Mode and Categories

From setup_status.json, note the `install_mode`.
Read categories from config/categories.json:
```bash
cat config/categories.json
```

═══════════════════════════════════════════════════════════════
PHASE 1: SELECT CATEGORY
═══════════════════════════════════════════════════════════════

### Step 1.1: Show Available Categories

```
═══════════════════════════════════════════════════════════════
       CREATE ARTIFACT
═══════════════════════════════════════════════════════════════

What type of artifact would you like to create?

Available categories:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. user_stories - User story documents for development teams
2. images - Generated images and diagrams
3. reports - Generated reports and summaries
4. exports - Exported data files
[Show any custom categories from categories.json]

Enter a number or category name:
```

Wait for user selection.

### Step 1.2: Confirm Category

```
Creating: [category_name]
Output formats available: [list from categories.json]
```

═══════════════════════════════════════════════════════════════
PHASE 2: SELECT OUTPUT FORMAT
═══════════════════════════════════════════════════════════════

### Step 2.1: Show Format Options

Based on the category's `output_formats`:

```
What format would you like?

Available formats for [category]:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. markdown (.md) - Rich text document
2. xlsx (.xlsx) - Excel spreadsheet
3. csv (.csv) - Comma-separated values
[etc. based on category]

Enter a number or format name:
```

Wait for user selection.

### Step 2.2: Format Availability Check

**If user selects xlsx:**
```
I'll try to generate an Excel file. If that doesn't work,
I'll create a CSV file instead that you can open in Excel.
```

**If user selects a format not available for this category:**
```
That format isn't available for [category].
Available formats are: [list]
Which would you like to use?
```

═══════════════════════════════════════════════════════════════
PHASE 3: GATHER REQUIREMENTS
═══════════════════════════════════════════════════════════════

### Step 3.1: Ask for Description

```
What should this artifact contain?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please describe what you need. For example:
- "Create a user story for the login feature"
- "Generate a summary report of the Q1 requirements"
- "Export all customer data to a spreadsheet"

Your description:
```

Wait for user input. Store as `artifact_description`.

### Step 3.2: Clarify if Needed

If the description is vague:
```
I want to make sure I create exactly what you need.
Could you tell me more about:
- What specific information should be included?
- Who is the audience for this artifact?
- Any particular structure or format preferences?
```

═══════════════════════════════════════════════════════════════
PHASE 4: SELECT REFERENCE SOURCES
═══════════════════════════════════════════════════════════════

### Step 4.1: Get Category Source Folders

From categories.json, get the `source_references` for the selected category.
Always include `unfiled_reference_md` (from `global_sources`).

### Step 4.2: Show Reference Options

```
Which reference documents should I use?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This category is configured to use:
✓ [folder1_reference_md] - [X] files
✓ [folder2_reference_md] - [Y] files
✓ unfiled_reference_md - [Z] files (always included)

Options:
a) Use all configured sources (recommended)
b) Let me select specific files
c) Search references by keyword

Your choice:
```

### Step 4.3: Handle Selection

**If "a" (all sources):**
Gather all markdown files from the configured source folders.

**If "b" (select specific):**
```
Available reference files:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[folder1_reference_md]:
1. requirements.md
2. specifications.md
3. user_guide.md

[folder2_reference_md]:
4. data_model.md
5. api_docs.md

[unfiled_reference_md]:
6. notes.md
7. meeting_summary.md

Enter file numbers (comma-separated) or "all":
```

**If "c" (search):**
```
Enter a keyword to search for:
```
Search through reference file contents and titles.
Show matching files and let user select.

═══════════════════════════════════════════════════════════════
PHASE 5: GENERATE ARTIFACT
═══════════════════════════════════════════════════════════════

### Step 5.1: Read Reference Content

For each selected reference file, read its content.
Build a context string with all the reference material.

### Step 5.2: Generate Content

Display:
```
Generating your artifact...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using [X] reference documents as context...
```

**Use the LLM to generate the artifact based on:**
- The user's description
- The reference document content
- The output format requirements
- The category type

**For user_stories format, include:**
- Title
- As a [user type]
- I want [functionality]
- So that [benefit]
- Acceptance criteria
- Notes/context

**For reports format, include:**
- Executive summary
- Key findings
- Details
- Recommendations
- Sources

**For exports format:**
- Structured data extracted from references
- Formatted according to output type

### Step 5.3: Format-Specific Generation

**For markdown output:**
Generate directly as markdown text.

**For xlsx output:**
```bash
# Generate with openpyxl (venv mode)
python -c "
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
# ... populate data ...
wb.save('../artifacts/[category]/[filename].xlsx')
"
```

Or in ephemeral mode:
```bash
uv run python -c "..."
```

If xlsx fails, fall back to CSV:
```
Excel generation encountered an issue.
Creating a CSV file instead (you can open this in Excel).
```

**For csv output:**
Generate CSV directly.

**For images:**
```
Note: I can describe diagrams and flowcharts in detail,
but actual image generation requires additional tools.
Would you like me to:
a) Create a detailed text description you can use
b) Generate a Mermaid diagram (text-based)
c) Suggest alternative approaches
```

═══════════════════════════════════════════════════════════════
PHASE 6: SAVE AND CONFIRM
═══════════════════════════════════════════════════════════════

### Step 6.1: Determine Filename

```
What would you like to name this artifact?
(I'll add the file extension automatically)

Suggested name: [auto-generated based on description]
```

Wait for user input or confirmation of suggested name.

### Step 6.2: Save Artifact

Save to: `../artifacts/[category]/[filename].[extension]`

```bash
# Create directory if needed
mkdir -p ../artifacts/[category]

# Write file
```

### Step 6.3: Confirm Success

```
═══════════════════════════════════════════════════════════════
       ARTIFACT CREATED
═══════════════════════════════════════════════════════════════

✓ Created: [filename].[extension]
📁 Location: artifacts/[category]/

[Preview of first few lines or summary]

Would you like to:
a) View the full artifact
b) Create another artifact
c) Edit/refine this artifact
d) Done for now
```

═══════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════

### If no reference files exist:
```
I don't have any reference documents to work with yet.

To create artifacts, I need reference markdown files generated
from your SharePoint documents.

Would you like to:
a) Run "sync references" to generate reference files
b) Create a blank artifact template
```

### If Excel generation fails:
```
I couldn't create an Excel file directly.
Creating a CSV file instead - you can open this in Excel
and save as .xlsx if needed.
```

### If artifact is too large:
```
This artifact is quite large. Would you like me to:
a) Split it into multiple files
b) Create a summary version
c) Continue with the full version
```

### If user tries to write to protected folder:
```
⚠️ I can't save files to [folder] - that's a protected
SharePoint folder. Artifacts go in the artifacts/ folder.

Saving to: artifacts/[category]/ instead.
```

═══════════════════════════════════════════════════════════════
ARTIFACT METADATA
═══════════════════════════════════════════════════════════════

Each artifact includes a header comment:
```
# Generated Artifact
# Category: [category]
# Created: [timestamp]
# Sources: [list of reference files used]
# Description: [user's description]
```

This helps track what was used to generate each artifact.
