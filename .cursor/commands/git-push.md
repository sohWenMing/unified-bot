---
name: Backup to Cloud
description: Upload your saves to GitHub/GitLab for backup and sharing
---

# Backup to Cloud (Git Push)

This command uploads your saved work to an online service (like GitHub) so it's backed up safely and can be accessed from anywhere.

## Trigger Phrases

Activate when user says:
- "Backup my work"
- "Backup"
- "Push changes"
- "Upload to cloud"
- "Save to GitHub"
- "Push to remote"
- "Sync to cloud"

## What this does:

1. Checks if you have saves to upload
2. Uploads your work to the cloud
3. Confirms success

## Instructions for Cursor:

### Step 1: Check Remote Configuration

```bash
git remote -v
```

If no remote configured:
```
You don't have cloud backup set up yet.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To set this up:
1. Go to GitHub.com and create a new repository
2. Copy the repository URL
3. Paste it here

Or say "skip" to continue without cloud backup.

Repository URL:
```

If user provides URL:
```bash
git remote add origin [URL]
git branch -M main
```

### Step 2: Check for Saves to Upload

```bash
git log origin/main..HEAD --oneline 2>/dev/null || git log --oneline -5
```

If nothing to push:
```
✓ You're all backed up!

Everything is already uploaded to the cloud.
No new saves to upload.
```
STOP here.

### Step 3: Show What Will Be Uploaded

```
Ready to backup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[X] saves to upload:
- [2 hours ago] Added login test
- [3 hours ago] Fixed checkout error

This will upload your work to: [remote URL]

Continue? (yes/no)
```

Wait for confirmation.

### Step 4: Upload to Cloud

First push (if branch doesn't exist remotely):
```bash
git push -u origin main
```

Regular push:
```bash
git push origin main
```

### Step 5: Confirm Success

```
✓ Backed up successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your work is now safely stored in the cloud.

Saves uploaded: [X]
Location: [remote URL]

Your work is now:
✓ Saved locally
✓ Backed up to the cloud
✓ Accessible from anywhere
```

## Error Handling:

### If remote has newer changes:
```
The cloud has updates you don't have locally.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Someone else (or you from another computer) made changes.
You need to get those changes first before uploading.

Would you like me to:
a) Get the latest changes and then upload yours
b) See what the differences are
c) Cancel for now
```

If user chooses (a):
```bash
git pull --rebase origin main
git push origin main
```

### If authentication fails:
```
I couldn't connect to the cloud repository.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This usually means you need to log in.

For GitHub:
1. Go to GitHub.com and make sure you're logged in
2. Check that you have access to this repository
3. Try again

Would you like more detailed instructions?
```

### If no remote configured:
```
You haven't set up cloud backup yet.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like to set it up now?

You'll need:
1. A GitHub account (free at github.com)
2. A new repository for this project

Say "setup backup" and I'll guide you through it.
```

### Setting Up Cloud Backup:

When user says "setup backup":

```
Let's set up cloud backup!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Create a repository
   Go to: https://github.com/new
   
   - Name it something like "my-bot-project"
   - Keep it Private (recommended)
   - Click "Create repository"
   
   Don't add any files - leave it empty.

Step 2: Copy the URL
   After creating, copy the URL that looks like:
   https://github.com/your-username/your-repo.git

Step 3: Paste it here
   
When you have the URL, paste it here:
```

When user provides URL:
```bash
git remote add origin [URL]
git branch -M main
git push -u origin main
```

Confirm:
```
✓ Cloud backup configured!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your work is now backed up to:
[URL]

From now on, just say "backup" to upload your latest saves.
```

## Safety Rules:

**NEVER force push** without explicit user confirmation:
```
⚠️ DANGER: Force push will overwrite cloud history!

This can cause problems if anyone else uses this repository.
Only do this if you're absolutely certain.

Type "I understand, force push" to proceed:
```

Only if user confirms:
```bash
git push --force origin main
```
