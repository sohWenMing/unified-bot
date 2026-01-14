#!/usr/bin/env python3
"""
Verification script for MarkItDown document conversion.

This script tests that the document conversion system is working properly.
It converts a sample text file and verifies the output.

Exit codes:
  0 - Verification passed
  1 - Conversion failed
  2 - Output verification failed
  3 - Missing dependencies
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import from ba_markitdown
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_dependencies():
    """Check that required dependencies are available."""
    missing = []
    
    try:
        import markitdown
    except ImportError:
        missing.append("markitdown")
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing.append("python-dotenv")
    
    return missing


def verify_conversion():
    """Verify that document conversion works."""
    from dotenv import load_dotenv
    
    # Load environment from bot root
    bot_root = Path(__file__).parent.parent
    env_path = bot_root / '.env'
    load_dotenv(env_path)
    
    # Check for API configuration (needed for cleanup)
    api_key = os.getenv('API_KEY')
    has_api = api_key and api_key != 'your_api_key_here'
    
    # Get sample file
    sample_file = Path(__file__).parent / 'sample_convert.txt'
    if not sample_file.exists():
        return {
            "success": False,
            "error": "Sample file not found",
            "details": str(sample_file)
        }
    
    # Create temp output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        # Import markitdown
        from markitdown import MarkItDown
        
        # Create converter
        md = MarkItDown()
        
        # Convert sample file
        result = md.convert(str(sample_file))
        
        # Write to temp file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        # Verify output has content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content or len(content) < 50:
            return {
                "success": False,
                "error": "Conversion produced no output",
                "details": f"Output length: {len(content)}"
            }
        
        # Check for expected content
        expected_phrases = ["Sample Document", "numbered list", "markdown"]
        found = [phrase for phrase in expected_phrases if phrase.lower() in content.lower()]
        
        if len(found) < 2:
            return {
                "success": False,
                "error": "Output missing expected content",
                "details": f"Found {len(found)} of {len(expected_phrases)} expected phrases"
            }
        
        return {
            "success": True,
            "message": "Document conversion is working",
            "has_api_cleanup": has_api,
            "output_length": len(content),
            "verified_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": type(e).__name__
        }
    finally:
        # Clean up temp file
        if os.path.exists(output_path):
            os.unlink(output_path)


def main():
    """Main verification function."""
    print("=" * 60)
    print("MarkItDown Verification Test")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        result = {
            "success": False,
            "test": "markitdown",
            "error": f"Missing dependencies: {', '.join(missing)}"
        }
        print(json.dumps(result, indent=2))
        sys.exit(3)
    
    print("Dependencies OK")
    print()
    
    # Run verification
    print("Testing document conversion...")
    result = verify_conversion()
    result["test"] = "markitdown"
    
    # Output result
    print()
    if result["success"]:
        print("[PASS] Document conversion verified!")
        if result.get("has_api_cleanup"):
            print("       API cleanup available")
        else:
            print("       (API cleanup not configured - basic conversion only)")
    else:
        print(f"[FAIL] {result.get('error', 'Unknown error')}")
        if result.get('details'):
            print(f"       Details: {result['details']}")
    
    print()
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
