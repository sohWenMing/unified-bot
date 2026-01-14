---
name: Save My Work
description: Save your current changes with a description (Git commit)
---

# Save My Work (Git Commit)

This command helps you save your current work as a checkpoint. Think of it as creating a snapshot of your work that you can return to later.

## Trigger Phrases

Activate when user says:
- "Save my work"
- "Save changes"
- "Commit changes"
- "Create checkpoint"
- "Save what I've done"

## What this does:

1. Shows you what files have changed
2. Asks for a brief description of your changes
3. Saves those changes as a checkpoint
4. Offers to back up to the cloud

## Instructions for Cursor:

### Step 1: Check for Changes

```bash
cd /path/to/bot && git status --porcelain
```

Parse the output:
- Lines starting with `??` = New files
- Lines starting with `M` = Modified files
- Lines starting with `D` = Deleted files
- Lines starting with `A` = Staged new files

### Step 2: Display Changes

If no changes:
```
✓ Everything is already saved!

There are no new changes since your last save.
Your work is safe.
```
STOP here.

If there are changes:
```
Here's what changed since your last save:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Modified files:
   - [file1]
   - [file2]

📄 New files:
   - [file3]

🗑️ Deleted files:
   - [file4]

[Total: X files changed]
```

### Step 3: Ask for Description

```
Please give this save a brief description.

Good examples:
- "Added login test"
- "Fixed checkout error"
- "Updated Q1 reports"

Your description:
```

Wait for user input.

### Step 4: Save Changes

```bash
git add -A
git commit -m "[user's description]"
```

### Step 5: Confirm Success

Get the commit hash:
```bash
git log -1 --format="%h"
```

Display:
```
✓ Saved successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Save ID: [commit hash]
Description: [user's message]

Your work is now saved locally.

Would you like to back up to the cloud?
(Say "backup" or "yes" to upload to GitHub)
```

If user says yes/backup:
Follow the git-push.md workflow.

## Error Handling:

### If git not initialized:
```
Version control isn't set up yet.
Say "setup" to configure everything, including version control.
```

### If commit fails:
```
I couldn't save your changes.
Error: [error message]

Would you like to try again or see more details?
```

### If user cancels:
```
Okay, I won't save anything right now.
Your changes are still there - just say "save my work" when you're ready.
```
