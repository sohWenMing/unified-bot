---
name: Sync References
description: Synchronize SharePoint documents with reference markdown files
---

# Sync SharePoint References

This command synchronizes the original SharePoint documents with their markdown reference copies. It detects new, updated, and orphaned files, allowing users to keep their reference library current.

## Trigger Phrases

Activate when user says:
- "Sync references"
- "Update references"
- "Sync my markdowns"
- "Update markdown files"
- "Refresh references"
- "Check for updates"
- "Sync SharePoint"

## Instructions for Cursor

═══════════════════════════════════════════════════════════════
PRE-SYNC CHECKS
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

### Step 2: Get Install Mode

From setup_status.json, note the `install_mode` value ("venv" or "ephemeral").
This determines how to run Python commands:
- venv: `python script.py`
- ephemeral: `uv run python script.py`

### Step 3: Read Protected Paths

```bash
cat config/protected_paths.json
```

Store the protected folder list - these are READ-ONLY source folders.

═══════════════════════════════════════════════════════════════
PHASE 1: SCAN AND COMPARE
═══════════════════════════════════════════════════════════════

### Step 1.1: Display Start Message

```
═══════════════════════════════════════════════════════════════
       SYNCING REFERENCES
═══════════════════════════════════════════════════════════════

Scanning SharePoint folders for changes...
```

### Step 1.2: Scan SharePoint Structure

```bash
python setup.py --scan-sharepoint --json
```

Parse the results to get:
- List of folders
- Files in each folder
- Root-level files

### Step 1.3: Scan Existing Reference Markdown Files

For each reference folder (ending in `_reference_md`), scan for existing markdown files and read their frontmatter to get:
- source_file
- source_path
- source_modified
- converted_at
- orphaned status

### Step 1.4: Compare and Categorize

Compare source files against markdown files and categorize into:

**NEW_FILES**: Source files that don't have a corresponding markdown file
**UPDATED_FILES**: Source files that are newer than their markdown file (compare source_modified timestamps)
**CURRENT_FILES**: Source files where markdown is up-to-date (markdown converted_at >= source_modified)
**ORPHANED_FILES**: Markdown files whose source no longer exists

═══════════════════════════════════════════════════════════════
PHASE 2: REPORT STATUS
═══════════════════════════════════════════════════════════════

### Step 2.1: Display Sync Summary

```
Sync Status Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 [folder1_name]
   ✓ Up-to-date: [X] files
   🆕 New: [Y] files
   🔄 Updated: [Z] files
   
📁 [folder2_name]
   ✓ Up-to-date: [X] files
   🆕 New: [Y] files
   🔄 Updated: [Z] files

📄 Root files (unfiled)
   ✓ Up-to-date: [X] files
   🆕 New: [Y] files

⚠️  Orphaned references: [N] files
   (Source files were removed but markdown kept for reference)
```

═══════════════════════════════════════════════════════════════
PHASE 3: HANDLE NEW FILES
═══════════════════════════════════════════════════════════════

If there are NEW_FILES:

### Step 3.1: Prompt for New Files

```
I found [X] new files that don't have markdown references yet:

New files:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [folder1]/document1.pdf
2. [folder1]/report.xlsx
3. [folder2]/presentation.pptx
...

Would you like me to generate markdown for these files?
a) Yes, generate all new references
b) Let me select which ones
c) Skip for now
```

### Step 3.2: Process Selection

**If user selects "a" (all):**
Process all new files.

**If user selects "b" (select):**
```
Enter the numbers of files to convert (comma-separated), or say "all":
```
Process selected files only.

**If user selects "c" (skip):**
Skip to next phase.

### Step 3.3: Generate New References

For each file to process:

Display progress:
```
Generating reference: [filename]... 
```

Determine the correct reference folder based on source location.

**venv mode:**
```bash
python ba_markitdown/main.py "../[source_folder]/[filename]" "../[folder]_reference_md/[filename].md" --frontmatter --cleanup --organization "[folder]_reference_md"
```

**ephemeral mode:**
```bash
uv run python ba_markitdown/main.py "../[source_folder]/[filename]" "../[folder]_reference_md/[filename].md" --frontmatter --cleanup --organization "[folder]_reference_md"
```

After each conversion, add source_modified timestamp to frontmatter:
```bash
# Get source file modification time and update frontmatter
```

Report result:
```
✓ Generated: [filename].md
```

═══════════════════════════════════════════════════════════════
PHASE 4: HANDLE UPDATED FILES
═══════════════════════════════════════════════════════════════

If there are UPDATED_FILES:

### Step 4.1: Prompt for Updated Files

```
I found [X] files that have been updated since their markdown was created:

Updated files:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [folder1]/document1.pdf (source: Jan 14, markdown: Jan 10)
2. [folder2]/report.xlsx (source: Jan 13, markdown: Jan 8)
...

Would you like me to regenerate the markdown for these files?
a) Yes, regenerate all updated references
b) Let me select which ones
c) Skip for now (keep existing markdown)
```

### Step 4.2: Process Selection

Same selection flow as new files.

### Step 4.3: Regenerate Updated References

For each file to regenerate:

Display:
```
Regenerating: [filename]...
(This will update the markdown with the latest content)
```

Run conversion with same command as new files.
The frontmatter will be updated with new timestamps.

Report:
```
✓ Regenerated: [filename].md
```

═══════════════════════════════════════════════════════════════
PHASE 5: HANDLE ORPHANED FILES
═══════════════════════════════════════════════════════════════

If there are ORPHANED_FILES:

### Step 5.1: Report Orphaned Files

```
⚠️  Orphaned References
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

These markdown files exist but their source documents were removed:

1. [folder1_reference_md]/old_document.md
   (Original: old_document.pdf - no longer exists)
   
2. [folder2_reference_md]/archived_report.md
   (Original: archived_report.xlsx - no longer exists)

These references have been marked as "orphaned" but are PRESERVED.
They may still contain useful information for generating artifacts.

Note: I will NEVER delete these files automatically.
If you want to remove them, you can do so manually.
```

### Step 5.2: Mark as Orphaned (if not already)

For orphaned files that aren't already marked:
```bash
# Update the frontmatter to set orphaned: true
```

**CRITICAL: NEVER delete markdown files, even if source is gone.**

═══════════════════════════════════════════════════════════════
PHASE 6: COMPLETION
═══════════════════════════════════════════════════════════════

### Step 6.1: Final Summary

```
═══════════════════════════════════════════════════════════════
       SYNC COMPLETE
═══════════════════════════════════════════════════════════════

Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ New references generated: [X]
✓ References regenerated: [Y]
⊘ Skipped (up-to-date): [Z]
⚠️  Orphaned (preserved): [N]

Your reference library is now up to date!

You can:
- Say "create artifact" to generate documents from these references
- Say "sync references" again anytime to check for updates
═══════════════════════════════════════════════════════════════
```

═══════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════

### If a conversion fails:

```
⚠️  Couldn't convert: [filename]
    Error: [error message]
    
This file was skipped. Would you like to:
a) Try again
b) Skip and continue with other files
c) Stop sync
```

### If no changes found:

```
✓ Everything is up to date!

All your SharePoint documents have current markdown references.
No action needed.
```

### If SharePoint folder not found:

```
I couldn't find the SharePoint folders. This might mean:
- The bot folder isn't in the SharePoint location yet
- The folder structure has changed

Please check that the bot folder is in the correct location
alongside your SharePoint folders.
```

═══════════════════════════════════════════════════════════════
FRONTMATTER STRUCTURE
═══════════════════════════════════════════════════════════════

Every generated markdown file has this frontmatter:

```yaml
---
source_reference:
  source_file: document.pdf
  source_path: ../original_folder/document.pdf
  source_modified: 2026-01-14T10:00:00
  converted_at: 2026-01-14T10:30:00
  organization: folder1_reference_md
  orphaned: false
  cleaned: true
---
```

This metadata enables:
- Tracking which source file generated this markdown
- Comparing timestamps for sync decisions
- Marking orphaned files without deleting them
- Knowing which reference folder the file belongs to
