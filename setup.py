#!/usr/bin/env python3
"""
Unified Setup Script for Bot Meta-Repository.

This script handles:
- Environment detection (Python, Node.js, uv, npm)
- Installation mode determination (venv vs ephemeral)
- SharePoint folder scanning
- Git initialization
- Configuration file management

All functions output JSON for easy parsing by Cursor commands.
"""

import subprocess
import sys
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


def get_bot_root() -> Path:
    """Get the bot repository root directory."""
    return Path(__file__).parent.resolve()


def get_sharepoint_root() -> Optional[Path]:
    """Get the SharePoint root directory (parent of bot folder)."""
    bot_root = get_bot_root()
    return bot_root.parent


# =============================================================================
# Environment Detection
# =============================================================================

def check_python_version() -> Dict[str, Any]:
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    return {
        "available": version >= (3, 10),
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "required": "3.10+",
        "message": f"Python {version.major}.{version.minor}.{version.micro} detected"
    }


def check_uv_available() -> Dict[str, Any]:
    """Check if uv package manager is available."""
    uv_path = shutil.which("uv")
    if uv_path:
        try:
            result = subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            version = result.stdout.strip() if result.returncode == 0 else "unknown"
            return {
                "available": True,
                "path": uv_path,
                "version": version,
                "message": f"uv found at {uv_path}"
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "message": "uv found but failed to execute"
            }
    return {
        "available": False,
        "message": "uv not found - will use pip or ephemeral mode"
    }


def check_pip_available() -> Dict[str, Any]:
    """Check if pip is available."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return {
                "available": True,
                "version": result.stdout.strip(),
                "message": "pip is available"
            }
    except Exception:
        pass
    return {
        "available": False,
        "message": "pip not available"
    }


def check_node_available() -> Dict[str, Any]:
    """Check if Node.js is available."""
    node_path = shutil.which("node")
    if node_path:
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return {
                    "available": True,
                    "path": node_path,
                    "version": version,
                    "message": f"Node.js {version} found"
                }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "message": "Node.js found but failed to execute"
            }
    return {
        "available": False,
        "message": "Node.js not found - required for Playwright tests",
        "install_guide": "Download from https://nodejs.org/"
    }


def check_npm_available() -> Dict[str, Any]:
    """Check if npm is available."""
    npm_path = shutil.which("npm")
    if npm_path:
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {
                    "available": True,
                    "path": npm_path,
                    "version": result.stdout.strip(),
                    "message": f"npm {result.stdout.strip()} found"
                }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "message": "npm found but failed to execute"
            }
    return {
        "available": False,
        "message": "npm not found"
    }


def check_git_available() -> Dict[str, Any]:
    """Check if git is available and repo status."""
    git_path = shutil.which("git")
    result = {
        "available": git_path is not None,
        "path": git_path,
        "repo_initialized": False,
        "has_backup": False
    }
    
    if git_path:
        bot_root = get_bot_root()
        
        # Check for .git directory
        git_dir = bot_root / ".git"
        result["repo_initialized"] = git_dir.exists()
        
        # Check for backup git directories in sub-repos
        ba_git_backup = bot_root / "ba_markitdown" / ".git_backup"
        cp_git_backup = bot_root / "cursor-playwright" / ".git_backup"
        result["has_backup"] = ba_git_backup.exists() or cp_git_backup.exists()
        
        # Check for existing git in sub-repos (needs backup)
        ba_git = bot_root / "ba_markitdown" / ".git"
        cp_git = bot_root / "cursor-playwright" / ".git"
        result["subrepos_need_backup"] = ba_git.exists() or cp_git.exists()
    
    return result


def check_venv_capability() -> Dict[str, Any]:
    """Check if we can create virtual environments."""
    bot_root = get_bot_root()
    test_venv_path = bot_root / ".venv_test"
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(test_venv_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and test_venv_path.exists():
            shutil.rmtree(test_venv_path, ignore_errors=True)
            return {
                "available": True,
                "message": "Virtual environment creation is supported"
            }
        else:
            return {
                "available": False,
                "error": result.stderr,
                "message": "Virtual environment creation failed"
            }
    except Exception as e:
        if test_venv_path.exists():
            shutil.rmtree(test_venv_path, ignore_errors=True)
        return {
            "available": False,
            "error": str(e),
            "message": f"Virtual environment test failed: {e}"
        }


def check_env_file() -> Dict[str, Any]:
    """Check if .env file exists and has required variables."""
    bot_root = get_bot_root()
    env_file = bot_root / ".env"
    env_example = bot_root / ".env.example"
    
    result = {
        "env_exists": env_file.exists(),
        "env_example_exists": env_example.exists(),
        "configured": False,
        "missing_vars": [],
        "has_markitdown_config": False,
        "has_playwright_config": False
    }
    
    # Variables for different components
    markitdown_vars = ["API_KEY", "BASE_URL", "LLM_MODEL"]
    playwright_vars = ["APP_URL", "TEST_USER_EMAIL", "TEST_USER_PASSWORD"]
    
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                content = f.read()
                
                # Check markitdown vars
                md_missing = []
                for var in markitdown_vars:
                    if f"{var}=" not in content or f"{var}=your_" in content:
                        md_missing.append(var)
                result["has_markitdown_config"] = len(md_missing) == 0
                
                # Check playwright vars
                pw_missing = []
                for var in playwright_vars:
                    if f"{var}=" not in content or f"{var}=your_" in content:
                        pw_missing.append(var)
                result["has_playwright_config"] = len(pw_missing) == 0
                
                result["missing_vars"] = md_missing + pw_missing
                result["configured"] = len(result["missing_vars"]) == 0
                
        except Exception as e:
            result["error"] = str(e)
    
    return result


# =============================================================================
# SharePoint Structure Detection
# =============================================================================

def scan_sharepoint_structure() -> Dict[str, Any]:
    """Scan the SharePoint folder structure (parent of bot folder)."""
    sharepoint_root = get_sharepoint_root()
    bot_root = get_bot_root()
    
    result = {
        "sharepoint_root": str(sharepoint_root),
        "folders": [],
        "files_at_root": [],
        "reference_folders_exist": [],
        "artifacts_folder_exists": False
    }
    
    if not sharepoint_root or not sharepoint_root.exists():
        result["error"] = "Could not find SharePoint root directory"
        return result
    
    try:
        for item in sharepoint_root.iterdir():
            # Skip the bot folder itself
            if item == bot_root:
                continue
            
            # Skip hidden files/folders
            if item.name.startswith('.'):
                continue
            
            if item.is_dir():
                # Check if it's a reference folder
                if item.name.endswith('_reference_md'):
                    result["reference_folders_exist"].append(item.name)
                elif item.name == 'artifacts':
                    result["artifacts_folder_exists"] = True
                elif item.name == 'unfiled_reference_md':
                    result["reference_folders_exist"].append(item.name)
                else:
                    # Regular SharePoint folder
                    result["folders"].append({
                        "name": item.name,
                        "path": str(item),
                        "file_count": len(list(item.glob('*')))
                    })
            else:
                # File at root level
                result["files_at_root"].append({
                    "name": item.name,
                    "path": str(item),
                    "size": item.stat().st_size
                })
    except Exception as e:
        result["error"] = str(e)
    
    return result


# =============================================================================
# Installation Mode Determination
# =============================================================================

def determine_install_mode(checks: Dict[str, Any]) -> str:
    """Determine the best installation mode based on environment checks."""
    if checks["uv"]["available"] and checks["venv"]["available"]:
        return "venv"
    elif checks["uv"]["available"]:
        return "ephemeral"
    elif checks["pip"]["available"] and checks["venv"]["available"]:
        return "venv_pip"
    else:
        return "ephemeral"


# =============================================================================
# Installation Functions
# =============================================================================

def install_python_dependencies(mode: str) -> Dict[str, Any]:
    """Install Python dependencies based on mode."""
    bot_root = get_bot_root()
    markitdown_dir = bot_root / "ba_markitdown"
    
    result = {
        "success": False,
        "mode": mode,
        "output": ""
    }
    
    try:
        if mode == "venv":
            # Use uv sync
            proc = subprocess.run(
                ["uv", "sync"],
                capture_output=True,
                text=True,
                cwd=str(markitdown_dir),
                timeout=300
            )
            result["output"] = proc.stdout + proc.stderr
            result["success"] = proc.returncode == 0
        elif mode == "venv_pip":
            # Create venv and install with pip
            venv_path = markitdown_dir / ".venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            pip_path = venv_path / "Scripts" / "pip.exe" if os.name == 'nt' else venv_path / "bin" / "pip"
            proc = subprocess.run(
                [str(pip_path), "install", "-e", "."],
                capture_output=True,
                text=True,
                cwd=str(markitdown_dir),
                timeout=300
            )
            result["output"] = proc.stdout + proc.stderr
            result["success"] = proc.returncode == 0
        else:
            # Ephemeral mode - nothing to install
            result["success"] = True
            result["output"] = "Ephemeral mode - dependencies loaded on demand"
            
    except Exception as e:
        result["error"] = str(e)
    
    return result


def install_node_dependencies() -> Dict[str, Any]:
    """Install Node.js dependencies."""
    bot_root = get_bot_root()
    playwright_dir = bot_root / "cursor-playwright"
    
    result = {
        "success": False,
        "output": ""
    }
    
    try:
        proc = subprocess.run(
            ["npm", "install"],
            capture_output=True,
            text=True,
            cwd=str(playwright_dir),
            timeout=300
        )
        result["output"] = proc.stdout + proc.stderr
        result["success"] = proc.returncode == 0
    except Exception as e:
        result["error"] = str(e)
    
    return result


def install_playwright_browsers() -> Dict[str, Any]:
    """Install Playwright browsers."""
    bot_root = get_bot_root()
    playwright_dir = bot_root / "cursor-playwright"
    
    result = {
        "success": False,
        "output": ""
    }
    
    try:
        proc = subprocess.run(
            ["npx", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            cwd=str(playwright_dir),
            timeout=600
        )
        result["output"] = proc.stdout + proc.stderr
        result["success"] = proc.returncode == 0
    except Exception as e:
        result["error"] = str(e)
    
    return result


# =============================================================================
# Git Operations
# =============================================================================

def backup_subrepo_git() -> Dict[str, Any]:
    """Backup git directories in sub-repositories."""
    bot_root = get_bot_root()
    result = {
        "ba_markitdown_backed_up": False,
        "cursor_playwright_backed_up": False
    }
    
    # Backup ba_markitdown/.git
    ba_git = bot_root / "ba_markitdown" / ".git"
    ba_backup = bot_root / "ba_markitdown" / ".git_backup"
    if ba_git.exists() and not ba_backup.exists():
        try:
            shutil.move(str(ba_git), str(ba_backup))
            result["ba_markitdown_backed_up"] = True
        except Exception as e:
            result["ba_markitdown_error"] = str(e)
    
    # Backup cursor-playwright/.git
    cp_git = bot_root / "cursor-playwright" / ".git"
    cp_backup = bot_root / "cursor-playwright" / ".git_backup"
    if cp_git.exists() and not cp_backup.exists():
        try:
            shutil.move(str(cp_git), str(cp_backup))
            result["cursor_playwright_backed_up"] = True
        except Exception as e:
            result["cursor_playwright_error"] = str(e)
    
    return result


def initialize_git() -> Dict[str, Any]:
    """Initialize git at bot root level."""
    bot_root = get_bot_root()
    result = {
        "success": False,
        "output": ""
    }
    
    try:
        # Check if already initialized
        git_dir = bot_root / ".git"
        if git_dir.exists():
            result["success"] = True
            result["output"] = "Git already initialized"
            return result
        
        # Initialize
        proc = subprocess.run(
            ["git", "init"],
            capture_output=True,
            text=True,
            cwd=str(bot_root)
        )
        result["output"] = proc.stdout + proc.stderr
        result["success"] = proc.returncode == 0
        
        # Initial commit if successful
        if result["success"]:
            subprocess.run(["git", "add", "-A"], cwd=str(bot_root))
            subprocess.run(
                ["git", "commit", "-m", "Initial commit: Bot meta-repository setup"],
                cwd=str(bot_root)
            )
            
    except Exception as e:
        result["error"] = str(e)
    
    return result


# =============================================================================
# Configuration Management
# =============================================================================

def save_setup_status(checks: Dict[str, Any], install_mode: str) -> Dict[str, Any]:
    """Save setup status to config/setup_status.json"""
    bot_root = get_bot_root()
    config_dir = bot_root / "config"
    config_dir.mkdir(exist_ok=True)
    status_file = config_dir / "setup_status.json"
    
    status = {
        "setup_complete": checks.get("env_file", {}).get("configured", False) and checks["python"]["available"],
        "install_mode": install_mode,
        "python_version": checks["python"]["version"],
        "node_version": checks.get("node", {}).get("version"),
        "uv_available": checks["uv"]["available"],
        "env_configured": checks.get("env_file", {}).get("configured", False),
        "verification": {
            "markitdown_test": None,
            "playwright_test": None,
            "api_test": None,
            "last_verified": None
        },
        "sharepoint_configured": False,
        "categories_configured": False,
        "git_initialized": checks.get("git", {}).get("repo_initialized", False),
        "last_setup": datetime.now().isoformat()
    }
    
    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)
    
    return status


def update_setup_status(updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update specific fields in setup_status.json"""
    bot_root = get_bot_root()
    status_file = bot_root / "config" / "setup_status.json"
    
    if status_file.exists():
        with open(status_file, "r") as f:
            status = json.load(f)
    else:
        status = {}
    
    # Deep merge updates
    for key, value in updates.items():
        if isinstance(value, dict) and key in status and isinstance(status[key], dict):
            status[key].update(value)
        else:
            status[key] = value
    
    status["last_updated"] = datetime.now().isoformat()
    
    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)
    
    return status


def save_protected_paths(folders: List[str]) -> None:
    """Save protected SharePoint folder paths."""
    bot_root = get_bot_root()
    config_file = bot_root / "config" / "protected_paths.json"
    
    config = {
        "protected_folders": folders,
        "protection_enabled": True,
        "configured_at": datetime.now().isoformat(),
        "notes": "These folders are original SharePoint folders and should NEVER be written to by the bot."
    }
    
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


def create_cursorignore(folders: List[str]) -> Dict[str, Any]:
    """Create .cursorignore file at SharePoint root to protect folders."""
    sharepoint_root = get_sharepoint_root()
    if not sharepoint_root:
        return {"success": False, "error": "Could not find SharePoint root directory"}
    
    cursorignore_path = sharepoint_root / ".cursorignore"
    
    content = """# SharePoint folders - PROTECTED (READ ONLY)
# These folders contain original source documents
# Cursor cannot write to, modify, or delete files in these folders

"""
    for folder in folders:
        content += f"{folder}/\n"
    
    content += """
# Allow reference markdown folders
!*_reference_md/

# Allow artifacts folder
!artifacts/

# Allow the bot folder
!unified-bot/
"""
    
    try:
        with open(cursorignore_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "path": str(cursorignore_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_reference_folders(folders: List[str]) -> Dict[str, Any]:
    """Create reference markdown folders and artifacts folder."""
    sharepoint_root = get_sharepoint_root()
    if not sharepoint_root:
        return {"success": False, "error": "Could not find SharePoint root directory"}
    
    created = []
    errors = []
    
    try:
        # Create reference folders for each SharePoint folder
        for folder in folders:
            ref_folder = sharepoint_root / f"{folder}_reference_md"
            ref_folder.mkdir(exist_ok=True)
            created.append(str(ref_folder))
        
        # Create unfiled reference folder
        unfiled = sharepoint_root / "unfiled_reference_md"
        unfiled.mkdir(exist_ok=True)
        created.append(str(unfiled))
        
        # Create artifacts folder with subfolders
        artifacts = sharepoint_root / "artifacts"
        for subfolder in ["user_stories", "reports", "exports", "images"]:
            (artifacts / subfolder).mkdir(parents=True, exist_ok=True)
        created.append(str(artifacts))
        
        return {"success": True, "created": created, "errors": errors}
    except Exception as e:
        return {"success": False, "error": str(e), "created": created}


# =============================================================================
# Main Functions
# =============================================================================

def run_all_checks() -> Dict[str, Any]:
    """Run all environment checks and return results."""
    checks = {
        "python": check_python_version(),
        "uv": check_uv_available(),
        "pip": check_pip_available(),
        "node": check_node_available(),
        "npm": check_npm_available(),
        "git": check_git_available(),
        "venv": check_venv_capability(),
        "env_file": check_env_file(),
        "sharepoint": scan_sharepoint_structure(),
        "timestamp": datetime.now().isoformat()
    }
    
    checks["recommended_mode"] = determine_install_mode(checks)
    
    # Generate human-readable summary
    summary = []
    
    if checks["python"]["available"]:
        summary.append(f"[OK] Python {checks['python']['version']}")
    else:
        summary.append(f"[!!] Python {checks['python']['version']} (need 3.10+)")
    
    if checks["node"]["available"]:
        summary.append(f"[OK] Node.js {checks['node']['version']}")
    else:
        summary.append("[!!] Node.js not found (needed for Playwright)")
    
    if checks["uv"]["available"]:
        summary.append("[OK] uv package manager available")
    else:
        summary.append("[--] uv not found (will use alternative)")
    
    if checks["venv"]["available"]:
        summary.append("[OK] Can create virtual environments")
    else:
        summary.append("[--] Using ephemeral mode")
    
    if checks["env_file"]["configured"]:
        summary.append("[OK] Environment configured")
    elif checks["env_file"]["env_exists"]:
        summary.append("[--] Environment file needs configuration")
    else:
        summary.append("[--] Environment file not created yet")
    
    if checks["git"]["repo_initialized"]:
        summary.append("[OK] Git initialized")
    else:
        summary.append("[--] Git not initialized")
    
    sp = checks["sharepoint"]
    summary.append(f"[--] SharePoint: {len(sp.get('folders', []))} folders, {len(sp.get('files_at_root', []))} root files")
    
    checks["summary"] = summary
    
    return checks


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Bot Meta-Repository Setup")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", action="store_true", help="Save status to config")
    parser.add_argument("--check-only", action="store_true", help="Only run checks, don't install")
    parser.add_argument("--install-python", action="store_true", help="Install Python dependencies")
    parser.add_argument("--install-node", action="store_true", help="Install Node dependencies")
    parser.add_argument("--install-playwright", action="store_true", help="Install Playwright browsers")
    parser.add_argument("--backup-git", action="store_true", help="Backup sub-repo git directories")
    parser.add_argument("--init-git", action="store_true", help="Initialize git at bot level")
    parser.add_argument("--scan-sharepoint", action="store_true", help="Scan SharePoint structure")
    parser.add_argument("--create-cursorignore", action="store_true", help="Create .cursorignore for protection")
    parser.add_argument("--create-folders", action="store_true", help="Create reference and artifact folders")
    
    args = parser.parse_args()
    
    # Run checks
    checks = run_all_checks()
    
    # Handle specific operations
    if args.install_python:
        result = install_python_dependencies(checks["recommended_mode"])
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Python installation: {'Success' if result['success'] else 'Failed'}")
        return
    
    if args.install_node:
        result = install_node_dependencies()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Node installation: {'Success' if result['success'] else 'Failed'}")
        return
    
    if args.install_playwright:
        result = install_playwright_browsers()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Playwright installation: {'Success' if result['success'] else 'Failed'}")
        return
    
    if args.backup_git:
        result = backup_subrepo_git()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Git backup: {result}")
        return
    
    if args.init_git:
        result = initialize_git()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Git init: {'Success' if result['success'] else 'Failed'}")
        return
    
    if args.scan_sharepoint:
        result = scan_sharepoint_structure()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("SharePoint Structure:")
            print(f"  Folders: {len(result.get('folders', []))}")
            print(f"  Root files: {len(result.get('files_at_root', []))}")
            for folder in result.get('folders', []):
                print(f"    - {folder['name']} ({folder['file_count']} files)")
        return
    
    if args.create_cursorignore:
        # Get folder names from scan
        sp_result = scan_sharepoint_structure()
        folder_names = [f["name"] for f in sp_result.get("folders", [])]
        result = create_cursorignore(folder_names)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"Created .cursorignore at: {result['path']}")
            else:
                print(f"Failed to create .cursorignore: {result.get('error', 'Unknown error')}")
        return
    
    if args.create_folders:
        # Get folder names from scan
        sp_result = scan_sharepoint_structure()
        folder_names = [f["name"] for f in sp_result.get("folders", [])]
        result = create_reference_folders(folder_names)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print("Created folders:")
                for folder in result.get("created", []):
                    print(f"  ✓ {folder}")
            else:
                print(f"Failed to create folders: {result.get('error', 'Unknown error')}")
        return
    
    # Save status if requested
    if args.save:
        save_setup_status(checks, checks["recommended_mode"])
    
    # Output results
    if args.json:
        output = {k: v for k, v in checks.items() if k != "summary"}
        print(json.dumps(output, indent=2))
    else:
        print("\n=== Bot Meta-Repository Environment Check ===\n")
        for line in checks["summary"]:
            print(line)
        print(f"\nRecommended mode: {checks['recommended_mode']}")
        print()
    
    # Exit code based on capability
    if checks["recommended_mode"] == "restricted":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
