#!/usr/bin/env python3
"""
Verification script for LLM API connectivity.

This script tests that the API key is configured correctly
and can connect to the LLM service.

Exit codes:
  0 - Verification passed
  1 - API key not configured
  2 - Connection failed
  3 - Authentication failed
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_env_configuration():
    """Check if .env has required variables."""
    from dotenv import load_dotenv
    
    # Load environment from bot root
    bot_root = Path(__file__).parent.parent
    env_path = bot_root / '.env'
    
    if not env_path.exists():
        return {
            "configured": False,
            "error": ".env file not found",
            "details": str(env_path)
        }
    
    load_dotenv(env_path)
    
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('BASE_URL')
    llm_model = os.getenv('LLM_MODEL')
    
    if not api_key or api_key == 'your_api_key_here':
        return {
            "configured": False,
            "error": "API_KEY not configured",
            "details": "Please add your API key to the .env file"
        }
    
    return {
        "configured": True,
        "api_key_length": len(api_key),
        "base_url": base_url or "default",
        "llm_model": llm_model or "default"
    }


def verify_api_connection():
    """Verify that we can connect to the LLM API."""
    from dotenv import load_dotenv
    from openai import OpenAI
    
    # Load environment
    bot_root = Path(__file__).parent.parent
    load_dotenv(bot_root / '.env')
    
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai/')
    llm_model = os.getenv('LLM_MODEL', 'gemini-2.0-flash')
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Simple API test - just list models or make minimal call
        # Using a very short prompt to minimize token usage
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "user", "content": "Say 'OK'"}
            ],
            max_tokens=10
        )
        
        # Check we got a response
        if response.choices and len(response.choices) > 0:
            return {
                "success": True,
                "message": "API connection successful",
                "model": llm_model,
                "response_received": True
            }
        else:
            return {
                "success": False,
                "error": "No response from API",
                "details": "API returned empty response"
            }
            
    except Exception as e:
        error_str = str(e)
        
        # Categorize errors
        if "401" in error_str or "unauthorized" in error_str.lower():
            return {
                "success": False,
                "error": "Authentication failed",
                "details": "API key may be invalid or expired"
            }
        elif "404" in error_str:
            return {
                "success": False,
                "error": "Model not found",
                "details": f"Model '{llm_model}' may not be available"
            }
        elif "connection" in error_str.lower() or "network" in error_str.lower():
            return {
                "success": False,
                "error": "Connection failed",
                "details": "Check your internet connection"
            }
        else:
            return {
                "success": False,
                "error": str(e),
                "details": type(e).__name__
            }


def main():
    """Main verification function."""
    print("=" * 60)
    print("API Connection Verification Test")
    print("=" * 60)
    print()
    
    # Check configuration first
    print("Checking configuration...")
    config = check_env_configuration()
    
    if not config.get("configured"):
        print(f"[FAIL] {config.get('error', 'Configuration error')}")
        if config.get('details'):
            print(f"       Details: {config['details']}")
        result = {
            "test": "api",
            "success": False,
            **config
        }
        print()
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    print(f"Configuration OK (key length: {config['api_key_length']})")
    print()
    
    # Test API connection
    print("Testing API connection...")
    result = verify_api_connection()
    result["test"] = "api"
    result["verified_at"] = datetime.now().isoformat()
    
    if result["success"]:
        print("[PASS] API connection verified!")
        print(f"       Model: {result.get('model', 'unknown')}")
    else:
        print(f"[FAIL] {result.get('error', 'Unknown error')}")
        if result.get('details'):
            print(f"       Details: {result['details']}")
    
    print()
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result["success"] else 2)


if __name__ == "__main__":
    # Check for openai dependency
    try:
        from dotenv import load_dotenv
        from openai import OpenAI
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Run: pip install openai python-dotenv")
        sys.exit(3)
    
    main()
