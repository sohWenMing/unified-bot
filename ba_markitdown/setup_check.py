#!/usr/bin/env python3
"""
Environment detection script for BA MarkItDown.
Checks system capabilities and determines the best installation mode.
"""

import subprocess
import sys
import json
import os
import shutil
from pathlib import Path
from datetime import datetime


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.resolve()


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    return {
        "available": version >= (3, 10),
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "required": "3.10+",
        "message": f"Python {version.major}.{version.minor}.{version.micro} detected"
    }


def check_uv_available():
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
        "message": "uv not found - will attempt to use pip or ephemeral mode"
    }


def check_pip_available():
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
    except Exception as e:
        pass
    return {
        "available": False,
        "message": "pip not available"
    }


def check_venv_capability():
    """Check if we can create virtual environments."""
    project_root = get_project_root()
    test_venv_path = project_root / ".venv_test"
    
    try:
        # Try to create a test venv
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(test_venv_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and test_venv_path.exists():
            # Clean up test venv
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
        # Clean up if exists
        if test_venv_path.exists():
            shutil.rmtree(test_venv_path, ignore_errors=True)
        return {
            "available": False,
            "error": str(e),
            "message": f"Virtual environment test failed: {e}"
        }


def check_package_install_capability():
    """
    Check if we can install packages.
    This is a non-destructive test that checks permissions.
    """
    uv_info = check_uv_available()
    
    if uv_info["available"]:
        # Test uv sync capability by checking if we can run uv commands
        try:
            project_root = get_project_root()
            result = subprocess.run(
                ["uv", "pip", "list"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(project_root)
            )
            # Even if it fails, uv being available means we can use ephemeral mode
            return {
                "available": True,
                "method": "uv",
                "message": "Package installation via uv is available"
            }
        except Exception:
            pass
    
    # Check pip in user mode
    pip_info = check_pip_available()
    if pip_info["available"]:
        return {
            "available": True,
            "method": "pip",
            "message": "Package installation via pip is available"
        }
    
    return {
        "available": False,
        "message": "No package installation method available - will use ephemeral mode"
    }


def check_env_file():
    """Check if .env file exists and has required variables."""
    project_root = get_project_root()
    # Check bot root (parent directory) for unified .env
    bot_root = project_root.parent
    env_file = bot_root / ".env"
    env_example = bot_root / ".env.example"
    
    result = {
        "env_exists": env_file.exists(),
        "env_example_exists": env_example.exists(),
        "configured": False,
        "missing_vars": []
    }
    
    required_vars = ["API_KEY", "BASE_URL", "LLM_MODEL"]
    
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                content = f.read()
                for var in required_vars:
                    if f"{var}=" not in content:
                        result["missing_vars"].append(var)
                    elif f"{var}=your_" in content or f"{var}=" in content and content.split(f"{var}=")[1].split("\n")[0].strip() == "":
                        result["missing_vars"].append(var)
                
                result["configured"] = len(result["missing_vars"]) == 0
        except Exception as e:
            result["error"] = str(e)
    
    if result["configured"]:
        result["message"] = "Environment file is configured"
    elif result["env_exists"]:
        result["message"] = f"Environment file exists but missing: {', '.join(result['missing_vars'])}"
    else:
        result["message"] = "Environment file not found - needs to be created from .env.example at bot root"
    
    return result


def check_git_available():
    """Check if git is available and repository is initialized."""
    git_path = shutil.which("git")
    
    result = {
        "git_available": git_path is not None,
        "repo_initialized": False,
        "remote_configured": False,
        "remote_url": None
    }
    
    if git_path:
        project_root = get_project_root()
        
        # Check if git repo exists
        try:
            check_repo = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                cwd=str(project_root),
                timeout=10
            )
            result["repo_initialized"] = check_repo.returncode == 0
        except Exception:
            pass
        
        # Check for remote
        if result["repo_initialized"]:
            try:
                check_remote = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    capture_output=True,
                    text=True,
                    cwd=str(project_root),
                    timeout=10
                )
                if check_remote.returncode == 0:
                    result["remote_configured"] = True
                    result["remote_url"] = check_remote.stdout.strip()
            except Exception:
                pass
    
    return result


def determine_install_mode(checks):
    """Determine the best installation mode based on checks."""
    if checks["uv"]["available"] and checks["venv"]["available"]:
        return "venv"  # Full virtual environment with uv
    elif checks["uv"]["available"]:
        return "ephemeral"  # Use uv run for ephemeral execution
    elif checks["pip"]["available"] and checks["venv"]["available"]:
        return "venv_pip"  # Virtual environment with pip
    else:
        return "restricted"  # Need IT assistance


def run_all_checks():
    """Run all environment checks and return results."""
    checks = {
        "python": check_python_version(),
        "uv": check_uv_available(),
        "pip": check_pip_available(),
        "venv": check_venv_capability(),
        "package_install": check_package_install_capability(),
        "env_file": check_env_file(),
        "git": check_git_available(),
        "timestamp": datetime.now().isoformat()
    }
    
    checks["recommended_mode"] = determine_install_mode(checks)
    
    # Generate human-readable summary
    summary = []
    
    if checks["python"]["available"]:
        summary.append(f"[OK] Python {checks['python']['version']}")
    else:
        summary.append(f"[!!] Python {checks['python']['version']} (need 3.10+)")
    
    if checks["uv"]["available"]:
        summary.append("[OK] uv package manager available")
    else:
        summary.append("[--] uv not found (will use alternative)")
    
    if checks["venv"]["available"]:
        summary.append("[OK] Can create virtual environments")
    else:
        summary.append("[!!] Cannot create virtual environments")
    
    if checks["env_file"]["configured"]:
        summary.append("[OK] Environment configured")
    elif checks["env_file"]["env_exists"]:
        summary.append("[--] Environment file needs configuration")
    else:
        summary.append("[--] Environment file not created yet")
    
    if checks["git"]["repo_initialized"]:
        if checks["git"]["remote_configured"]:
            summary.append("[OK] Git configured with remote")
        else:
            summary.append("[--] Git initialized but no remote")
    else:
        summary.append("[--] Git not initialized")
    
    mode_descriptions = {
        "venv": "Full installation with virtual environment (recommended)",
        "ephemeral": "Ephemeral mode with uv run (no permanent installation)",
        "venv_pip": "Virtual environment with pip",
        "restricted": "Restricted environment - may need IT assistance"
    }
    
    summary.append(f"\nRecommended mode: {mode_descriptions.get(checks['recommended_mode'], checks['recommended_mode'])}")
    
    checks["summary"] = summary
    
    return checks


def save_setup_status(checks):
    """Save setup status to .setup_status.json"""
    project_root = get_project_root()
    status_file = project_root / ".setup_status.json"
    
    status = {
        "setup_complete": checks["env_file"]["configured"] and checks["python"]["available"],
        "install_mode": checks["recommended_mode"],
        "env_configured": checks["env_file"]["configured"],
        "remote_configured": checks["git"].get("remote_configured", False),
        "remote_url": checks["git"].get("remote_url"),
        "last_setup_check": checks["timestamp"],
        "python_version": checks["python"]["version"],
        "uv_available": checks["uv"]["available"]
    }
    
    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)
    
    return status


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check environment for BA MarkItDown")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", action="store_true", help="Save status to .setup_status.json")
    args = parser.parse_args()
    
    checks = run_all_checks()
    
    if args.save:
        save_setup_status(checks)
    
    if args.json:
        # Remove summary for clean JSON output
        output = {k: v for k, v in checks.items() if k != "summary"}
        print(json.dumps(output, indent=2))
    else:
        print("\n=== BA MarkItDown Environment Check ===\n")
        for line in checks["summary"]:
            print(line)
        print()
    
    # Return exit code based on whether we can run
    if checks["recommended_mode"] == "restricted":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
