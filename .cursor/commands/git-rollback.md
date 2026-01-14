---
name: Undo Changes
description: Go back to a previous save (Git revert/rollback)
---

# Undo Changes (Git Rollback)

This command helps you go back to an earlier version of your work if something went wrong.

⚠️ **Use carefully** - this will undo changes made after the selected save.

## Trigger Phrases

Activate when user says:
- "Undo changes"
- "Undo my changes"
- "Go back"
- "Rollback"
- "Restore previous version"
- "Undo last change"
- "Revert"

## What this does:

1. Shows your recent saves
2. Lets you choose which version to go back to
3. Creates a safety backup before changing anything
4. Restores your work to the selected version

## Instructions for Cursor:

### Step 1: Check for Uncommitted Changes

```bash
git status --porcelain
```

If there are uncommitted changes:
```
⚠️ You have unsaved changes:
- [list modified files]

What would you like to do?
a) Save these changes first, then undo
b) Discard these changes and proceed with undo
c) Cancel

```

Handle user choice before proceeding.

### Step 2: Show Recent Saves

```bash
git log --pretty=format:"%h|%ar|%s" -10
```

Display:
```
Which version do you want to go back to?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [2 hours ago] Added login test (current)
2. [Yesterday] Fixed checkout error
3. [3 days ago] Updated Q1 reports
4. [1 week ago] Initial setup

Enter the number of the version you want to restore:
```

Wait for user selection.

### Step 3: Show What Will Be Undone

Based on user selection, show commits that will be undone:

```bash
git log --oneline [selected_hash]..HEAD
```

Display:
```
⚠️ WARNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Going back to: "[selected message]"

This will undo these changes:
- [2 hours ago] Added login test
- [4 hours ago] Fixed typo

The undone changes will be safely backed up, so you can
recover them if needed.

Are you sure you want to continue? (yes/no)
```

If user says no: STOP immediately.

### Step 4: Create Safety Backup

```bash
git branch backup-$(date +%Y%m%d-%H%M%S)
```

Display:
```
✓ Created safety backup: backup-[timestamp]
  (You can recover from here if needed)
```

### Step 5: Perform Safe Revert

**IMPORTANT**: Use revert (safe) instead of reset (destructive)

For single commit undo:
```bash
git revert HEAD --no-edit
```

For multiple commits:
```bash
git revert --no-commit [oldest_hash]^..HEAD
git commit -m "Reverted to: [selected message]"
```

### Step 6: Confirm Success

```bash
git log -1
```

Display:
```
✓ Successfully restored!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your work is now back to: "[selected message]"

The changes that were undone are saved in:
- Backup branch: backup-[timestamp]

If you need to get them back, just let me know!
```

## Scenario Handlers:

### Undo Just the Last Change

If user says something like "undo the last change":

```bash
git revert HEAD --no-edit
```

Display:
```
✓ Undone: [last commit message]

Your previous change has been undone.
The undone changes are still saved in history if you need them.
```

### Discard Uncommitted Changes

If user wants to discard unsaved work:

```
⚠️ This will permanently discard your unsaved changes:
- [list files]

This cannot be undone. Are you sure? (yes/no)
```

If confirmed:
```bash
git checkout -- .
git clean -fd
```

## Error Handling:

### If no commits to undo:
```
There's nothing to undo yet.
Your project is at the initial state.
```

### If revert has conflicts:
```
There's a conflict while undoing changes.

This happens when the same file was modified in different ways.
I can help you resolve this. Would you like to:
a) Keep your current version
b) Keep the older version
c) See both versions and choose
```

### Recovery Information:
Always remind user:
```
Your backup is saved at: backup-[timestamp]
If you change your mind, let me know and I can restore it.
```

## Safety Rules:

**NEVER do these:**
- `git push --force`
- `git reset --hard` without backup
- Delete backup branches automatically

**ALWAYS do these:**
- Create backup branch before any destructive operation
- Require explicit confirmation
- Show exactly what will be changed
- Provide recovery instructions
