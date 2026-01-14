#!/usr/bin/env python3
"""
⚠️ OBSOLETE - This script is no longer used.

This test script used the old folder structure (to_be_converted/, converted/).
The unified bot now uses SharePoint folders → reference markdown folders.

For verification tests, use:
- test_files/verify_markitdown.py (for conversion testing)
- test_files/verify_api.py (for API connectivity)
- test_files/verify_playwright.js (for Playwright testing)

These are run automatically during setup.
"""

import os
import sys
import shutil
from pathlib import Path
from get_python import get_python_path

def run_setup_test():
    """Run a test conversion to verify everything works."""
    project_root = Path(__file__).parent.resolve()
    test_file = project_root / "test_files" / "test.xlsx"
    to_be_converted = project_root / "to_be_converted"
    converted = project_root / "converted" / "unfiled"
    
    # Check if test file exists
    if not test_file.exists():
        print("[ERROR] Test file not found: test_files/test.xlsx")
        return False
    
    print("Running setup test...")
    print()
    
    # Step 1: Copy test file
    print("1. Copying test file to to_be_converted folder...")
    try:
        shutil.copy2(test_file, to_be_converted / "test.xlsx")
        print("   [OK] Test file copied")
    except Exception as e:
        print(f"   [ERROR] Failed to copy test file: {e}")
        return False
    
    # Step 2: Run conversion
    print()
    print("2. Testing conversion...")
    converted.mkdir(parents=True, exist_ok=True)
    output_file = converted / "test.xlsx.md"
    
    python_cmd = get_python_path()
    import subprocess
    
    try:
        result = subprocess.run(
            [
                python_cmd,
                "main.py",
                str(to_be_converted / "test.xlsx"),
                str(output_file),
                "--cleanup",
                "--frontmatter",
                "--organization", "unfiled"
            ],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode == 0:
            if output_file.exists():
                print("   [OK] Conversion successful!")
                print(f"   [OK] Output file created: {output_file}")
            else:
                print("   [WARNING] Conversion reported success but output file not found")
                return False
        else:
            print("   [ERROR] Conversion failed")
            if result.stderr:
                print(f"   Error details: {result.stderr[:500]}")  # Limit error output
            return False
            
    except subprocess.TimeoutExpired:
        print("   [ERROR] Conversion timed out (took longer than 2 minutes)")
        return False
    except Exception as e:
        print(f"   [ERROR] Conversion error: {e}")
        return False
    
    # Step 3: Cleanup
    print()
    print("3. Cleaning up test files...")
    try:
        # Remove from to_be_converted
        test_input = to_be_converted / "test.xlsx"
        if test_input.exists():
            test_input.unlink()
            print("   [OK] Removed test file from to_be_converted/")
        
        # Remove from converted
        if output_file.exists():
            output_file.unlink()
            print("   [OK] Removed test file from converted/unfiled/")
        
        # Remove empty unfiled folder if it exists and is empty
        if converted.exists() and not any(converted.iterdir()):
            converted.rmdir()
            print("   [OK] Cleaned up empty unfiled folder")
            
    except Exception as e:
        print(f"   [WARNING] Cleanup warning: {e}")
        # Don't fail the test if cleanup fails
    
    print()
    print("[SUCCESS] Setup test completed successfully!")
    print("   Everything is working correctly. You're ready to convert files!")
    return True

if __name__ == "__main__":
    success = run_setup_test()
    sys.exit(0 if success else 1)
