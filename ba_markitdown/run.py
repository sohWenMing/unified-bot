#!/usr/bin/env python3
"""
Helper script that automatically uses the virtual environment if it exists.
This allows commands to work seamlessly without manual activation.
"""

import sys
import os
from pathlib import Path

def find_venv_python():
    """Find the Python executable in the virtual environment."""
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

def main():
    """Run the requested script with the appropriate Python."""
    venv_python = find_venv_python()
    
    # Get the script to run and its arguments
    if len(sys.argv) < 2:
        print("Usage: python run.py <script> [args...]")
        sys.exit(1)
    
    script = sys.argv[1]
    args = sys.argv[2:]
    
    # Build the command
    import subprocess
    cmd = [venv_python, script] + args
    
    # Execute
    sys.exit(subprocess.run(cmd).returncode)

if __name__ == "__main__":
    main()
