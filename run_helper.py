#!/usr/bin/env python3
"""
Run Helper - Execution mode utility for bot commands.

This module provides utilities for determining the correct execution mode
and building appropriate command strings based on the setup configuration.

Usage:
    from run_helper import get_execution_mode, build_python_command, build_node_command

    mode = get_execution_mode()
    cmd = build_python_command("ba_markitdown/main.py", ["input.pdf", "output.md"])
    
Or from command line:
    python run_helper.py python ba_markitdown/main.py input.pdf output.md
    python run_helper.py node cursor-playwright/test.js
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional, Tuple


def get_bot_root() -> Path:
    """Get the bot repository root directory."""
    return Path(__file__).parent.resolve()


def get_execution_mode() -> str:
    """
    Determine the execution mode from setup_status.json.
    
    Returns:
        str: One of 'venv', 'venv_pip', or 'ephemeral'
    """
    bot_root = get_bot_root()
    status_file = bot_root / 'config' / 'setup_status.json'
    
    if not status_file.exists():
        return 'ephemeral'  # Default to ephemeral if not configured
    
    try:
        with open(status_file, 'r') as f:
            status = json.load(f)
        
        mode = status.get('install_mode')
        if mode in ('venv', 'venv_pip', 'ephemeral'):
            return mode
        return 'ephemeral'  # Default if invalid or null
        
    except (json.JSONDecodeError, IOError):
        return 'ephemeral'


def is_venv_mode() -> bool:
    """Check if running in venv mode (not ephemeral)."""
    mode = get_execution_mode()
    return mode in ('venv', 'venv_pip')


def is_ephemeral_mode() -> bool:
    """Check if running in ephemeral mode."""
    return get_execution_mode() == 'ephemeral'


def build_python_command(script: str, args: Optional[List[str]] = None) -> List[str]:
    """
    Build the appropriate Python command based on execution mode.
    
    Args:
        script: Path to the Python script (relative to bot root)
        args: List of arguments to pass to the script
        
    Returns:
        List[str]: Command parts ready for subprocess
    """
    mode = get_execution_mode()
    args = args or []
    
    if mode in ('venv', 'venv_pip'):
        return ['python', script] + args
    else:  # ephemeral
        return ['uv', 'run', 'python', script] + args


def build_node_command(script: str, args: Optional[List[str]] = None) -> List[str]:
    """
    Build the appropriate Node.js command.
    
    Args:
        script: Path to the Node.js script or npm command
        args: List of arguments
        
    Returns:
        List[str]: Command parts ready for subprocess
    """
    args = args or []
    
    # Node commands typically use npx in both modes
    if script.endswith('.js') or script.endswith('.ts'):
        return ['node', script] + args
    else:
        return ['npx', script] + args


def build_playwright_command(test_path: Optional[str] = None, 
                             headed: bool = False,
                             debug: bool = False) -> List[str]:
    """
    Build a Playwright test command.
    
    Args:
        test_path: Optional path to specific test file
        headed: Run in headed mode
        debug: Run in debug mode
        
    Returns:
        List[str]: Command parts ready for subprocess
    """
    cmd = ['npx', 'playwright', 'test']
    
    if test_path:
        cmd.append(test_path)
    
    if headed:
        cmd.append('--headed')
    
    if debug:
        cmd.append('--debug')
    
    return cmd


def run_command(cmd: List[str], 
                cwd: Optional[str] = None,
                capture_output: bool = False,
                timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """
    Run a command and return results.
    
    Args:
        cmd: Command parts
        cwd: Working directory
        capture_output: Whether to capture stdout/stderr
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or str(get_bot_root()),
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        
        stdout = result.stdout if capture_output else ''
        stderr = result.stderr if capture_output else ''
        
        return result.returncode, stdout, stderr
        
    except subprocess.TimeoutExpired:
        return -1, '', 'Command timed out'
    except Exception as e:
        return -1, '', str(e)


def main():
    """Command line interface for run_helper."""
    if len(sys.argv) < 3:
        print("Usage: python run_helper.py <python|node> <script> [args...]")
        print("")
        print("Examples:")
        print("  python run_helper.py python ba_markitdown/main.py input.pdf output.md")
        print("  python run_helper.py node cursor-playwright/test.js")
        print("  python run_helper.py playwright test --headed")
        print("")
        print(f"Current mode: {get_execution_mode()}")
        sys.exit(1)
    
    command_type = sys.argv[1].lower()
    script = sys.argv[2]
    args = sys.argv[3:]
    
    if command_type == 'python':
        cmd = build_python_command(script, args)
    elif command_type == 'node':
        cmd = build_node_command(script, args)
    elif command_type == 'playwright':
        # Special case for playwright
        headed = '--headed' in args
        debug = '--debug' in args
        test_args = [a for a in args if a not in ('--headed', '--debug')]
        test_path = test_args[0] if test_args else None
        cmd = build_playwright_command(test_path, headed, debug)
        cmd = ['cd', 'cursor-playwright', '&&'] + cmd
    else:
        print(f"Unknown command type: {command_type}")
        print("Use: python, node, or playwright")
        sys.exit(1)
    
    print(f"Mode: {get_execution_mode()}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 40)
    
    # Execute the command
    if command_type == 'playwright':
        # For playwright, we need to run in the cursor-playwright directory
        cwd = str(get_bot_root() / 'cursor-playwright')
        cmd = build_playwright_command(
            test_args[0] if test_args else None,
            '--headed' in args,
            '--debug' in args
        )
        returncode, _, _ = run_command(cmd, cwd=cwd)
    else:
        returncode, _, _ = run_command(cmd)
    
    sys.exit(returncode)


if __name__ == "__main__":
    main()
