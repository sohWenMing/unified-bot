---
name: Sync Converted Files
description: Check which SharePoint files have been converted to markdown and their status
---

# Sync Converted Files

This command shows you the status of all SharePoint files - which have been converted to markdown references, which haven't, and identifies any orphaned conversions.

## Trigger Phrases

Activate when user says:
- "Sync my files"
- "Check my files"
- "Show file status"
- "What's converted"
- "List converted files"
- "Show conversion status"

## Instructions for Cursor

═══════════════════════════════════════════════════════════════
STEP 1: GATHER FILE LISTS
═══════════════════════════════════════════════════════════════

### Step 1.1: Scan SharePoint Structure

```bash
python setup.py --scan-sharepoint --json
```

Parse results to get:
- SharePoint folders and their files
- Root-level files

### Step 1.2: Scan Reference Markdown Folders

```bash
# Find all reference markdown folders
ls -d ../*_reference_md 2>/dev/null
ls -d ../unfiled_reference_md 2>/dev/null

# List all markdown files in reference folders
find ../*_reference_md -name "*.md" -type f 2>/dev/null
find ../unfiled_reference_md -name "*.md" -type f 2>/dev/null
```

### Step 1.3: Read Frontmatter for Tracking

For each converted markdown file, read the frontmatter to get:
- source_file: Original filename
- source_path: Path to original file
- organization: Which reference folder it's in

═══════════════════════════════════════════════════════════════
STEP 2: COMPARE AND CATEGORIZE
═══════════════════════════════════════════════════════════════

For each SharePoint file, check if corresponding markdown exists:

**CONVERTED**: Source files that have corresponding markdown files in reference folders
**NOT_CONVERTED**: Source files without markdown files
**ORPHANED**: Markdown files whose source no longer exists in SharePoint folders

═══════════════════════════════════════════════════════════════
STEP 3: DISPLAY STATUS
═══════════════════════════════════════════════════════════════

```
═══════════════════════════════════════════════════════════════
       FILE CONVERSION STATUS
═══════════════════════════════════════════════════════════════

✓ Converted Files: [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 [folder1]
   - document1.pdf → folder1_reference_md/document1.md
   - report.xlsx → folder1_reference_md/report.md

📁 [folder2]
   - specs.docx → folder2_reference_md/specs.md

📄 Root files
   - notes.txt → unfiled_reference_md/notes.md

📄 Not Yet Converted: [Y]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 [folder1]
   - presentation.pptx
   - image.png

📁 [folder2]
   - data.csv

📄 Root files
   - meeting_summary.pdf

⚠️ Orphaned Conversions: [Z]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 folder1_reference_md/
   - old_report.md
   (Original: old_report.pdf - no longer exists in SharePoint)
   
📄 unfiled_reference_md/
   - archived_notes.md
   (Original: archived_notes.txt - no longer exists)
   
Note: These markdown files are preserved because they may
still contain useful information for generating artifacts.
```

═══════════════════════════════════════════════════════════════
STEP 4: OFFER ACTIONS
═══════════════════════════════════════════════════════════════

```
What would you like to do?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a) Convert the [Y] unconverted files
b) View details of a specific file
c) Sync references (check for updates)
d) Done for now
```

**If user chooses (a):**
Trigger the `convert-files.md` workflow with the unconverted files.

**If user chooses (b):**
```
Which file would you like to see details for?
(Enter the filename or path)
```

Show details including:
- File location in SharePoint
- File size
- Last modified date
- Conversion status
- If converted: when, where the markdown is, organization

**If user chooses (c):**
Trigger the `sync-references.md` workflow to check for updates.

═══════════════════════════════════════════════════════════════
NOTES
═══════════════════════════════════════════════════════════════

**Orphaned files are NEVER deleted automatically.**
They may contain valuable information even if the original SharePoint file is gone.

**To clean up orphaned files manually:**
The user must manually delete them if desired.
The system will not offer automatic deletion.

**Difference from sync-references:**
- `sync-files` - Shows status only (read-only check)
- `sync-references` - Actually syncs and converts files (updates markdown)
