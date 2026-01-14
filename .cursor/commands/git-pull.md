---
name: Get Latest
description: Download the latest changes from cloud/GitHub
---

# Get Latest (Git Pull)

This command downloads the latest changes from your cloud backup (GitHub/GitLab) so you have the most up-to-date version.

## Trigger Phrases

Activate when user says:
- "Get latest"
- "Pull changes"
- "Sync from cloud"
- "Download updates"
- "Get updates"
- "Update from cloud"

## What this does:

1. Checks if you have unsaved local changes
2. Downloads the latest changes from the cloud
3. Shows you what was updated
4. Helps resolve any conflicts if they occur

## Instructions for Cursor

### Step 1: Check Remote Configuration

```bash
git remote -v
```

If no remote configured:
```
You don't have cloud backup set up yet.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To get updates from the cloud, you need to connect to a repository first.

Would you like to set up cloud backup now?
Say "setup backup" or "backup" to get started.
```
STOP and wait for user.

### Step 2: Check for Local Changes

```bash
git status --porcelain
```

If there are uncommitted changes:
```
You have unsaved local changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [list modified/new files]

What would you like to do?
a) Save these changes first, then get updates
b) Stash these changes temporarily, get updates, then restore them
c) Cancel (keep your current state)

```
Wait for user choice.

**If user chooses (a):**
Follow git-commit.md workflow to save changes first.

**If user chooses (b):**
```bash
git stash push -m "Temporary stash before pull"
```
Display: "✓ Temporarily saved your changes"

**If user chooses (c):**
STOP - don't pull.

### Step 3: Pull Updates

```bash
git pull origin main
```

Or if on different branch:
```bash
git branch --show-current
```
Then pull that branch:
```bash
git pull origin [current-branch]
```

### Step 4: Display Results

**If successful:**
```bash
git log HEAD@{1}..HEAD --oneline
```

Display:
```
✓ Successfully updated from cloud!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Here's what was updated:
- [commit 1] - [message]
- [commit 2] - [message]

Files changed:
- [file1]
- [file2]

You're now up to date with the cloud version.
```

**If already up to date:**
```
✓ You're already up to date!

Your local version matches the cloud version.
No updates needed.
```

**If conflicts occur:**
```
⚠️ CONFLICT DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

There are conflicts between your local changes and the cloud version.

Conflicted files:
- [file1]
- [file2]

What this means:
Both you and someone else (or you from another computer) changed
the same files. I need your help to decide which version to keep.

Options:
a) Keep your local version (discard cloud changes)
b) Keep cloud version (discard your local changes)
c) See both versions and choose manually
d) Cancel and resolve later

Which would you like?
```

**Handle conflict resolution:**

**If user chooses (a) - Keep local:**
```bash
git checkout --ours [file]
git add [file]
git commit -m "Resolved conflict: kept local version"
```

**If user chooses (b) - Keep cloud:**
```bash
git checkout --theirs [file]
git add [file]
git commit -m "Resolved conflict: kept cloud version"
```

**If user chooses (c) - Manual:**
```
I'll show you both versions. Open these files in your editor:

Local version: [file]
Cloud version: [show diff]

Edit the file to combine both changes, then tell me when you're done.
```
Wait for confirmation, then:
```bash
git add [file]
git commit -m "Resolved conflict manually"
```

### Step 5: Restore Stashed Changes (if applicable)

If changes were stashed in Step 2:
```bash
git stash pop
```

Display:
```
✓ Restored your temporary changes

Your local changes are back and combined with the cloud updates.
```

If stash conflicts:
```
There's a conflict between your stashed changes and the updates.

Would you like to:
a) Keep your stashed changes
b) Keep the updated version
c) See both and choose manually
```

## Error Handling

### If remote has no updates:
```
The cloud repository is already up to date.
Your local version matches what's in the cloud.
```

### If network error:
```
Couldn't connect to the cloud right now.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This might be a network issue. Your local work is safe.

Try again in a few minutes, or check your internet connection.
```

### If authentication fails:
```
Authentication failed.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I couldn't authenticate with GitHub/GitLab.

You might need to:
1. Log in to GitHub/GitLab in your browser
2. Check your credentials or access tokens
3. Set up SSH keys if using SSH

Would you like help setting up authentication?
```

## Safety Notes

- Never force pull or overwrite without user confirmation
- Always show what will be updated before pulling
- Preserve local changes unless user explicitly chooses to discard
- Use stash for temporary storage, not permanent deletion
