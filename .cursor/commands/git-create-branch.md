---
name: Create Branch
description: Create a new workspace branch to try changes without affecting main
---

# Create New Branch

This command creates a new "branch" - think of it as a separate workspace where you can make changes without affecting your main project.

## Trigger Phrases

Activate when user says:
- "Create branch"
- "New branch"
- "Create workspace"
- "Make a branch"
- "Start new branch"
- "Create new workspace"

## What this does:

1. Shows your current branch
2. Asks for a name for your new branch
3. Creates the branch
4. Switches you to the new branch
5. Confirms you're now working in the new space

## When to use this:

- Testing new features
- Trying risky changes
- Working on multiple things at once
- Preparing changes before merging to main

## Instructions for Cursor

### Step 1: Show Current Status

```bash
git branch --show-current
git status --short
```

Display:
```
Current Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You're currently on branch: [branch-name]

[Show any uncommitted changes if present]
```

### Step 2: Ask for Branch Name

```
What would you like to name the new branch?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Naming guidelines:
• Use lowercase letters and hyphens
• Be descriptive about what you're working on
• Examples:
  - "add-payment-test"
  - "fix-login-bug"
  - "experiment-new-selectors"
  - "update-q1-reports"

Branch name:
```

Wait for user input.

### Step 3: Validate Name

**Check if branch already exists:**
```bash
git branch --list [user-input]
```

**If branch exists:**
```
A branch named "[name]" already exists.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like to:
a) Switch to the existing branch
b) Choose a different name
c) Cancel
```

**If user chooses (a):**
```bash
git checkout [name]
```
Display: "✓ Switched to existing branch: [name]"
STOP here.

**If user chooses (b):**
Go back to Step 2.

**If user chooses (c):**
STOP - don't create branch.

**If name is invalid (contains spaces, special chars):**
```
That branch name isn't valid.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Branch names should:
• Use lowercase letters
• Use hyphens instead of spaces
• Avoid special characters

Example: "add-payment-test" (not "Add Payment Test")

Would you like to try again?
```

**If name is valid and doesn't exist:**
Proceed to Step 4.

### Step 4: Create and Switch

```bash
git checkout -b [branch-name]
```

### Step 5: Confirm Success

```bash
git branch --show-current
```

Display:
```
✓ Created new branch: [branch-name]
✓ Switched to: [branch-name]

You're now working in a separate workspace.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes you make here won't affect your main branch
until you choose to merge them.

Your branches:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
git branch
```

Display the branch list with current branch marked.

```
The * indicates your current branch.

To go back to your previous branch:
Say "switch to [previous-branch-name]" or use git commands.

To merge your changes back to main later:
Say "merge branch" or "combine branches"
```

## Error Handling

### If checkout fails:
```
Couldn't create the branch.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error: [error message]

Common causes:
• Uncommitted changes that conflict
• Git repository issues

Would you like to:
a) Save your current changes first, then try again
b) See more details about the error
c) Cancel
```

### If user cancels:
```
Okay, I won't create a branch right now.
You're still on: [current-branch]
```

## Additional Information

### Show Branch Tips

After successful creation, optionally show:
```
Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Make changes freely - they're isolated to this branch
• Save your work normally - commits go to this branch
• When ready, merge back to main
• You can switch between branches anytime
```

## Safety Notes

- Never delete branches without explicit user request
- Always show current branch before creating new one
- Warn if there are uncommitted changes that might cause issues
- Provide clear instructions for switching back
