# ⚠️ OBSOLETE - This README is no longer current

**This documentation is for the old standalone ba_markitdown repository.**

The bot has been unified into a meta-repository. For current documentation, see:
- `bot/README.md` - Main documentation  
- `bot/.cursor/commands/help.md` - Command reference

The old workflow (to_be_converted/ → converted/) has been replaced with SharePoint folders → reference markdown folders.

---

# BA MarkItDown (OLD)

A simple tool that converts your documents (PDFs, Word, Excel, PowerPoint, images) into a format that works great with AI assistants.

## What Does This Do?

When you're working with AI tools, they work best with plain text. This tool takes your various documents and converts them to Markdown format - a simple text format that AI understands really well.

**Just drop your files in a folder, say "convert my files", and you're done.**

---

## Quick Start (3 Steps)

### Step 1: Open This Project in Cursor

Open the Cursor editor and open this project folder.

### Step 2: Say "Setup"

In the Cursor chat, just type:
> setup

The AI assistant will guide you through everything. You'll need to:
- Get a free API key from Google (the assistant will show you where)
- Paste that key into a configuration file (never in the chat!)

### Step 3: Start Converting!

1. Put your files in the `to_be_converted` folder
2. In the chat, say:
   > convert my files
3. Answer a few questions about how you want to organize them
4. Find your converted files in the `converted` folder

That's it!

---

## What Can I Say?

Here are the things you can ask the assistant to do:

### Converting Files
| Say This | What Happens |
|----------|--------------|
| "Convert my files" | Converts all files in the to_be_converted folder |
| "Convert report.pdf" | Converts a specific file |
| "Sync my files" | Shows which files have been converted |

### Saving Your Work
| Say This | What Happens |
|----------|--------------|
| "Save my work" | Saves a checkpoint of your current files |
| "Show my history" | Shows all your previous saves |
| "Undo my changes" | Goes back to a previous checkpoint |

### Cloud Backup
| Say This | What Happens |
|----------|--------------|
| "Backup my work" | Uploads your saves to the cloud |
| "Get latest" | Downloads the latest from the cloud |
| "Setup backup" | Connects to GitHub for cloud storage |

### Getting Help
| Say This | What Happens |
|----------|--------------|
| "Help" | Shows all available commands |
| "Help with converting" | Explains how to convert files |
| "Help with saving" | Explains how to save and restore |
| "Show available models" | Shows AI models you can use |

---

## Supported File Types

This tool can convert:
- PDF documents
- Microsoft Word (.docx, .doc)
- Microsoft Excel (.xlsx, .xls)
- Microsoft PowerPoint (.pptx, .ppt)
- Images (.png, .jpg, .gif) - extracts and describes text
- HTML files
- Plain text files
- Audio files (.mp3, .wav) - requires additional setup
- Video files (.mp4, .mov) - requires additional setup

---

## Folder Structure

```
📁 Your Project
├── 📁 to_be_converted     ← Put files here to convert
├── 📁 converted           ← Find your markdown files here
│   ├── 📁 by_project      ← Organized by project name
│   ├── 📁 by_user_story   ← Organized by user story
│   └── 📁 unfiled         ← For quick conversions
└── 📄 .env                ← Your configuration (keep private!)
```

---

## Important Security Note

**Never paste your API key in the chat window!**

When you get your API key, always put it directly in the `.env` file using your text editor. Pasting it in the chat would send it through external services and compromise its security.

If you accidentally paste an API key in the chat:
1. Go to your API provider immediately
2. Revoke/delete that key
3. Generate a new one
4. Put the new key in your `.env` file

---

## Troubleshooting

### "I can't convert files"
Say "setup" to make sure everything is configured correctly.

### "My API key isn't working"
Open the `.env` file and check that your API_KEY is filled in correctly.

### "Audio/video files aren't working"
These require ffmpeg to be installed. The assistant will try to help, or you can skip these files.

### "I made a mistake and want to go back"
Say "undo my changes" to restore a previous version.

### "I need more help"
Just say "help" in the chat and the assistant will guide you!

---

## For Technical Users

<details>
<summary>Click to expand technical details</summary>

### Manual Setup

If you prefer to set things up manually:

```bash
# Install dependencies
uv sync

# Copy environment template
cp ../.env.example ../.env

# Edit .env with your API key
# Then run conversions
python main.py input.pdf output.md --cleanup --frontmatter
```

### Command Line Options

```bash
python main.py <input_file> <output_file> [options]

Options:
  --cleanup, -c       Run LLM cleanup pass on output
  --frontmatter, -f   Add YAML tracking metadata
  --organization, -o  Set organization path for frontmatter
  --json, -j          Output results as JSON
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| API_KEY | Your LLM API key | (required) |
| BASE_URL | API endpoint URL | Google Gemini endpoint |
| LLM_MODEL | Model to use | gemini-2.0-flash |

### Setup Check

```bash
# Check environment status
python setup_check.py

# Save status to .setup_status.json
python setup_check.py --save

# Output as JSON
python setup_check.py --json
```

</details>

---

## Getting Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in your `.env` file (not in the chat!)

The free tier is generous and should cover normal usage.

---

## Questions?

Just ask the assistant! Say "help" anytime to get guidance.
