---
name: Convert Files
description: Convert SharePoint documents to markdown reference files
---

# Convert Files to Markdown

This command converts documents from your SharePoint folders to LLM-friendly markdown format, storing them in the corresponding reference markdown folders.

## Trigger Phrases

Activate when user says:
- "Convert my files"
- "Convert files"
- "Transform my documents"
- "Turn my files into markdown"
- "Process my files"
- "Convert [specific filename]"

## Instructions for Cursor

═══════════════════════════════════════════════════════════════
PRE-CONVERSION CHECKS
═══════════════════════════════════════════════════════════════

### Step 1: Check Setup Status

```bash
cat config/setup_status.json
```

If `setup_complete` is false or `env_configured` is false:
```
You haven't completed setup yet. Would you like to run setup first?
Say "setup" to get started.
```
STOP and wait for user.

### Step 2: Get Install Mode

Note the `install_mode` from setup_status.json:
- "venv" → use `python ba_markitdown/main.py`
- "ephemeral" → use `uv run python ba_markitdown/main.py`

### Step 3: Read Protected Paths

```bash
cat config/protected_paths.json
```

Get the list of SharePoint folders (protected folders).

### Step 4: Scan SharePoint Structure

```bash
python setup.py --scan-sharepoint --json
```

Parse results to get:
- SharePoint folders and their files
- Root-level files (for unfiled_reference_md)

═══════════════════════════════════════════════════════════════
PHASE 1: SHOW AVAILABLE FILES
═══════════════════════════════════════════════════════════════

### Step 1.1: Display Files from SharePoint

```
═══════════════════════════════════════════════════════════════
       CONVERT FILES TO MARKDOWN
═══════════════════════════════════════════════════════════════

I found files in your SharePoint folders:

📁 [folder1_name] - [X] files
   - document1.pdf
   - report.xlsx
   - presentation.pptx

📁 [folder2_name] - [Y] files
   - specs.docx
   - data.csv

📄 Root level files - [Z] files
   - notes.txt
   - meeting_summary.pdf

What would you like to do?
a) Convert all files from all folders
b) Convert files from specific folders
c) Convert only new files (skip already converted)
d) Select specific files to convert
```

Wait for user selection.

═══════════════════════════════════════════════════════════════
PHASE 2: CHECK FOR EXISTING CONVERSIONS
═══════════════════════════════════════════════════════════════

### Step 2.1: Check Reference Folders

For each file, check if markdown already exists in corresponding reference folder:

```bash
# For folder1 files, check folder1_reference_md
ls -la ../folder1_reference_md/ 2>/dev/null | grep "[filename].md"

# For root files, check unfiled_reference_md
ls -la ../unfiled_reference_md/ 2>/dev/null | grep "[filename].md"
```

### Step 2.2: Report Existing Conversions

If markdown files exist:
```
Some files have been converted before:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 [folder1]
   - document1.pdf → ../folder1_reference_md/document1.md (exists)
   - report.xlsx → (not converted yet)

📄 Root files
   - notes.txt → ../unfiled_reference_md/notes.md (exists)

For files that already have markdown, would you like to:
a) Skip them (keep existing markdown)
b) Regenerate and overwrite
c) Create new copies with different names
```

═══════════════════════════════════════════════════════════════
PHASE 3: DETERMINE OUTPUT LOCATIONS
═══════════════════════════════════════════════════════════════

### Step 3.1: Map Files to Reference Folders

For each file to convert, determine the correct reference folder:

**Files in SharePoint folders:**
- Source: `../folder1/document.pdf`
- Output: `../folder1_reference_md/document.md`
- Organization: `folder1_reference_md`

**Root-level files:**
- Source: `../notes.txt`
- Output: `../unfiled_reference_md/notes.md`
- Organization: `unfiled_reference_md`

### Step 3.2: Ensure Reference Folders Exist

```bash
# Create reference folders if they don't exist
mkdir -p ../folder1_reference_md
mkdir -p ../folder2_reference_md
mkdir -p ../unfiled_reference_md
```

═══════════════════════════════════════════════════════════════
PHASE 4: CONFIRM AND CONVERT
═══════════════════════════════════════════════════════════════

### Step 4.1: Confirmation

```
Ready to convert:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files to convert: [X]

📁 [folder1] → folder1_reference_md/
   - document1.pdf
   - report.xlsx

📁 [folder2] → folder2_reference_md/
   - specs.docx

📄 Root files → unfiled_reference_md/
   - notes.txt

⚠️ Note: This will use your API credits.
Large files may take a few minutes.

Proceed? (yes/no)
```

Wait for confirmation.

### Step 4.2: Execute Conversions

For each file, show progress:
```
Converting files...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/4] Converting document1.pdf...
```

**venv mode:**
```bash
python ba_markitdown/main.py "../folder1/document1.pdf" "../folder1_reference_md/document1.md" --cleanup --frontmatter --organization "folder1_reference_md"
```

**ephemeral mode:**
```bash
uv run python ba_markitdown/main.py "../folder1/document1.pdf" "../folder1_reference_md/document1.md" --cleanup --frontmatter --organization "folder1_reference_md"
```

**Important:** Use relative paths `../` to go up from bot folder to SharePoint level.

After each file:
```
✓ Converted: document1.pdf → folder1_reference_md/document1.md

[2/4] Converting report.xlsx...
```

═══════════════════════════════════════════════════════════════
PHASE 5: HANDLE ERRORS
═══════════════════════════════════════════════════════════════

### Error Types and Handling

**If conversion fails:**
```
⚠️ Couldn't convert: [filename]

Would you like to:
a) See the technical details
b) Skip and continue with other files
c) Stop here
```

**For ffmpeg errors (audio/video):**
```
This file requires special software (ffmpeg) that isn't installed.

Would you like to:
a) Skip this file
b) Get instructions for installing ffmpeg
```

**For password-protected files:**
```
This file appears to be password-protected.
Please provide an unprotected version to convert.
```

**If SharePoint folder not found:**
```
I couldn't find the SharePoint folder: [folder_name]

Please check that:
- The bot folder is in the correct location
- SharePoint folders are at the same level as the bot folder
- Run "setup" to reconfigure SharePoint paths
```

═══════════════════════════════════════════════════════════════
PHASE 6: REPORT RESULTS
═══════════════════════════════════════════════════════════════

```
═══════════════════════════════════════════════════════════════
       CONVERSION COMPLETE
═══════════════════════════════════════════════════════════════

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Successfully converted: [X] files
  📁 folder1_reference_md/
     - document1.pdf → document1.md
     - report.xlsx → report.md
  
  📁 folder2_reference_md/
     - specs.docx → specs.md
  
  📄 unfiled_reference_md/
     - notes.txt → notes.md

⊘ Skipped: [Y] files (already converted)

✗ Failed: [Z] files
  - video.mp4 (needs ffmpeg)

Your markdown reference files are ready!
They're stored in the reference folders alongside your SharePoint folders.

Would you like to:
a) View one of the converted files
b) Convert more files
c) Sync references (to check for updates)
d) Done for now
```

═══════════════════════════════════════════════════════════════
SINGLE FILE CONVERSION
═══════════════════════════════════════════════════════════════

When user says "Convert report.pdf":

1. Scan SharePoint structure to find the file
2. If not found:
   ```
   I couldn't find "report.pdf" in your SharePoint folders.
   
   Please check:
   - Is the file in one of your SharePoint folders?
   - Is the bot folder in the correct location?
   
   Or tell me which folder it's in and I'll convert it.
   ```

3. If found in folder1:
   - Determine output: `../folder1_reference_md/report.md`
   - Check if already converted
   - Run conversion
   - Report result

4. If found at root level:
   - Determine output: `../unfiled_reference_md/report.md`
   - Convert and report

═══════════════════════════════════════════════════════════════
SUPPORTED FILE TYPES
═══════════════════════════════════════════════════════════════

When user asks "what can you convert?":

```
Supported File Types:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Documents
   - PDF (.pdf)
   - Microsoft Word (.docx, .doc)
   - Plain text (.txt)
   - HTML (.html)

📊 Spreadsheets
   - Microsoft Excel (.xlsx, .xls)
   - CSV (.csv)

📽️ Presentations
   - Microsoft PowerPoint (.pptx, .ppt)

🖼️ Images
   - PNG, JPG, GIF
   (Extracts text and describes content)

🎵 Audio/Video (requires ffmpeg)
   - MP3, WAV, MP4, MOV
   (Transcribes speech to text)
```

═══════════════════════════════════════════════════════════════
NOTES
═══════════════════════════════════════════════════════════════

**File Organization:**
- Files from SharePoint folders → corresponding `*_reference_md` folders
- Root-level files → `unfiled_reference_md` folder
- This matches the structure used by `sync-references.md`

**Frontmatter:**
Each converted markdown file includes frontmatter with:
- source_file: Original filename
- source_path: Relative path to original
- source_modified: Timestamp of source file
- converted_at: Conversion timestamp
- organization: Which reference folder it belongs to

This metadata enables sync operations and artifact generation.
