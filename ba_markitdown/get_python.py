#!/usr/bin/env python3
"""
Helper script that returns the path to the Python executable to use.
Automatically detects and uses the virtual environment if it exists.
"""

import sys
from pathlib import Path

def get_python_path():
    """Get the path to the Python executable to use."""
    project_root = Path(__file__).parent.resolve()
    
    # Check for venv in common locations
    venv_paths = [
        project_root / ".venv",
        project_root / "venv",
        project_root / "env",
    ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
            if python_exe.exists():
                return str(python_exe)
            
            # Unix/Mac
            python_exe = venv_path / "bin" / "python"
            if python_exe.exists():
                return str(python_exe)
    
    # Fall back to system Python
    return sys.executable

if __name__ == "__main__":
    print(get_python_path())
