---
name: Show History
description: See the history of all your saves (Git log)
---

# Show History (Git Log)

This command shows you all the saves (checkpoints) you've created, so you can see what was changed and when.

## Trigger Phrases

Activate when user says:
- "Show history"
- "Show my history"
- "View history"
- "What did I change"
- "Show recent changes"
- "Show saves"
- "Show commits"
- "What have I done"

## What this does:

Shows your recent saves with:
- When the save was made
- What was changed (the description)
- A unique ID for each save

## Instructions for Cursor:

### Step 1: Get History

```bash
git log --pretty=format:"%h|%ar|%s" -10
```

Parse each line (format: hash|time_ago|message)

### Step 2: Display History

```
Your Recent Saves
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [2 hours ago] Added login test
   ID: abc1234

2. [Yesterday] Fixed checkout error  
   ID: def5678

3. [3 days ago] Updated Q1 reports
   ID: ghi9012

4. [1 week ago] Initial setup
   ID: jkl3456

[Showing last 10 saves]

Would you like to:
a) See more saves
b) See details of a specific save
c) Go back to an earlier version
```

### Step 3: Handle Follow-up

**If user wants more saves:**
```bash
git log --pretty=format:"%h|%ar|%s" -20
```
Show next 10.

**If user wants details of a save:**
```
Which save? (Enter the number or ID)
```

When user selects:
```bash
git show --stat [hash]
```

Display:
```
Save Details: [hash]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description: [message]
Created: [full date/time]

Files changed:
- ba_markitdown/main.py (modified)
- tests/login.spec.ts (added)
- config/old.json (deleted)

Would you like to see what exactly changed in each file?
```

**If user wants to go back:**
Direct to git-rollback.md command.

## Error Handling:

### If no history exists:
```
No saves yet!

You haven't saved any work yet. After making changes,
say "save my work" to create your first checkpoint.
```

### If git not initialized:
```
Version control isn't set up yet.
Say "setup" to get started.
```
