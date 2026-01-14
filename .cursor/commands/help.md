---
name: Help
description: Show all available commands and how to use the bot
---

# Help - Bot Command Guide

This command shows all available commands and provides guidance on how to use the bot.

## Trigger Phrases

Activate when user says:
- "Help"
- "What can you do"
- "Show commands"
- "List commands"
- "How do I use this"
- "Guide"

## Instructions for Cursor

### Display Main Help Menu

```
═══════════════════════════════════════════════════════════════
       BOT COMMAND GUIDE
═══════════════════════════════════════════════════════════════

Here's everything I can help you with:

📦 SETUP & CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "setup" to configure the bot (first time only)

📄 DOCUMENT CONVERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "convert my files" to turn documents into markdown
Say "sync my files" to check conversion status
Supported: PDF, Word, Excel, PowerPoint, images, text

🔄 SHAREPOINT REFERENCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "sync references" to update markdown from SharePoint
(Converts new files, updates changed files, preserves orphans)

📝 ARTIFACTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "create artifact" to generate:
- User stories
- Reports  
- Data exports (Excel, CSV)
- And more

Note: Artifacts are generated from reference markdown folders
(*_reference_md/), not directly from SharePoint folders. Make sure
to convert/sync your SharePoint files first!

🧪 AUTOMATED TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "generate test" to create a new automated test
Say "run all tests" to check your application
Say "run test headed" to watch a test execute
Say "analyze results" to understand test failures

💾 VERSION CONTROL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "save my work" to create a checkpoint
Say "show history" to see past saves
Say "undo changes" to go back to a previous version
Say "backup" to upload to GitHub
Say "get latest" to download updates from cloud
Say "create branch" to start a new workspace

❓ GETTING MORE HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say "help with [topic]" for specific guidance:
- "help with converting"
- "help with testing"
- "help with artifacts"
- "help with saving"

What would you like to do?
═══════════════════════════════════════════════════════════════
```

## Topic-Specific Help

### Help with Converting

```
DOCUMENT CONVERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How It Works:
The bot converts files from your SharePoint folders into markdown
reference files. These reference files are used for generating artifacts.

Getting Started:
1. Your files are already in SharePoint folders (at the same level as bot/)
2. Say "convert my files" to convert them to markdown
3. Files are automatically organized into reference folders:
   - Files from [folder1] → [folder1]_reference_md/
   - Files from [folder2] → [folder2]_reference_md/
   - Root-level files → unfiled_reference_md/

What You Can Say:
• "Convert my files" - Convert all files from SharePoint folders
• "Convert report.pdf" - Convert a specific file (I'll find it)
• "Sync my files" - Check what's been converted
• "Sync references" - Update markdown from SharePoint (full sync)

Supported Files:
• PDF, Word (.docx), Excel (.xlsx), PowerPoint
• Images (extracts/describes text)
• HTML, plain text
• Audio/Video (requires ffmpeg)

Tips:
• Large files may take a few minutes
• Reference markdown files are stored alongside SharePoint folders
• Already converted files can be skipped or regenerated
• Use "sync references" to keep markdown files up-to-date
```

### Help with Testing

```
AUTOMATED TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Creating Tests:
1. Say "generate test"
2. Describe what you want to test step by step
3. I'll verify it works and create the test
4. Run "run test headed" to watch it execute

Running Tests:
• "Run all tests" - Run everything
• "Run test headed" - Watch a test execute
• "Analyze results" - Understand failures

When Tests Fail:
• FALSE NEGATIVE: Feature works but test fails
  → Say "Self-Heal [Test Name]"
  
• TRUE NEGATIVE: Feature is actually broken
  → Report to development team

Self-Healing:
Tests can fix themselves when the UI changes but
the feature still works. Just confirm the behavior
works manually, then run the self-heal command.
```

### Help with Artifacts

```
ARTIFACT GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What Are Artifacts?
Generated documents created from your reference markdown files:
• User stories for development teams
• Reports and summaries
• Data exports (Excel, CSV)
• Images and diagrams (descriptions)

IMPORTANT - How Artifacts Work:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Artifacts are generated from REFERENCE MARKDOWN FOLDERS, not
directly from your original SharePoint folders.

Here's the workflow:
1. Original documents are in SharePoint folders (read-only)
2. Documents are converted to markdown → stored in *_reference_md/ folders
3. Artifacts are generated from these markdown references

Why This Matters:
• Each artifact category is configured to use specific reference folders
• The unfiled_reference_md folder is available to all categories
• You must convert/sync SharePoint files to markdown first
• Then artifacts can be generated from the markdown references

How to Create:
1. First, ensure your SharePoint files are converted:
   • Say "convert my files" or "sync references"
   • This creates markdown references in *_reference_md/ folders

2. Then create your artifact:
   • Say "create artifact"
   • Choose a category (user_stories, reports, etc.)
   • Choose output format (markdown, xlsx, csv)
   • Describe what you need
   • I'll generate it using the reference markdown files

Categories:
• user_stories - Development requirements
• reports - Summaries and analyses
• exports - Data in spreadsheet format
• images - Diagram descriptions

Each category uses specific reference folders (configured during setup).

Tips:
• Always sync references first: "sync references"
• This ensures markdown files are up-to-date
• Artifacts use the latest markdown content
• Be specific about what you need
• Artifacts are saved in the artifacts/ folder
```

### Help with Saving

```
VERSION CONTROL (Git)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Think of saves as checkpoints you can return to.

Basic Commands:
• "Save my work" - Create a checkpoint
• "Show history" - See all checkpoints
• "Undo changes" - Go back to a checkpoint
• "Backup" - Upload to GitHub
• "Get latest" - Download updates from cloud
• "Create branch" - Start a new workspace for experiments

How It Works:
1. Make changes (convert files, create tests, etc.)
2. Say "save my work"
3. Describe your changes ("Added Q1 reports")
4. Done! You can always go back if needed.

Cloud Backup:
• Say "backup" to upload to GitHub
• Say "get latest" to download updates from cloud
• Your work is then safe even if computer fails
• Access from anywhere
• Share with team

Branches (Separate Workspaces):
• Say "create branch" to start experimenting safely
• Changes in branches don't affect your main work
• Perfect for trying new features or risky changes
• Merge back to main when ready

Tips:
• Save after important changes
• Use descriptive messages
• Backup regularly for safety
• Get latest before starting new work
• Use branches for experimental changes
• Rollback creates a safety copy first
```

## Quick Reference Card

When user asks for "cheat sheet" or "quick reference":

```
QUICK REFERENCE CARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Say This              | To Do This                    |
|-----------------------|-------------------------------|
| "setup"               | Configure everything          |
| "convert my files"    | Convert documents to markdown |
| "sync references"     | Update SharePoint markdowns   |
| "create artifact"     | Generate user stories, etc.   |
| "generate test"       | Create automated test         |
| "run all tests"       | Execute all tests             |
| "run test headed"     | Watch a test execute          |
| "save my work"        | Create checkpoint             |
| "show history"        | View past saves               |
| "undo changes"        | Restore previous version      |
| "backup"              | Upload to GitHub              |
| "get latest"          | Download updates from cloud   |
| "create branch"       | Start new workspace           |
| "help"                | Show this guide               |

Folders:
• SharePoint folders - Your original documents (read-only)
• *_reference_md/ - Converted markdown references
• unfiled_reference_md/ - References for root-level files
• artifacts/ - Generated artifacts here

Remember:
• Never paste API keys in chat
• Original SharePoint folders are read-only
• Say "help with [topic]" for detailed guidance
```
