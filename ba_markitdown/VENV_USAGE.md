# Automatic Virtual Environment Usage

This project is configured to **automatically use the virtual environment** for all Python commands. Users never need to manually activate it.

## How It Works

The `get_python.py` script automatically detects and returns the path to the correct Python executable:
- If `.venv` exists → uses `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (Unix/Mac)
- Otherwise → falls back to system Python

## Usage

Instead of:
```bash
python main.py input.pdf output.md
```

Use:
```bash
$(python get_python.py) main.py input.pdf output.md
```

Or directly:
```bash
.venv/Scripts/python.exe main.py input.pdf output.md  # Windows
.venv/bin/python main.py input.pdf output.md           # Unix/Mac
```

## For AI Assistants

When running Python commands, always use one of these methods:

1. **Use get_python.py helper:**
   ```bash
   $(python get_python.py) script.py [args]
   ```

2. **Direct venv path (Windows):**
   ```bash
   .venv\Scripts\python.exe script.py [args]
   ```

3. **Direct venv path (Unix/Mac):**
   ```bash
   .venv/bin/python script.py [args]
   ```

**Never ask users to manually activate the environment.** Always detect and use it automatically.
