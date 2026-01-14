#!/usr/bin/env python3
"""
List available Google Gemini models.

This script shows both known model names and attempts to fetch
the current list from the API (if API key is configured).
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from bot-level .env
_env_path = Path(__file__).parent.parent / '.env'
load_dotenv(_env_path)

# Known Google Gemini model names (as of 2025)
KNOWN_MODELS = {
    "Gemini 2.0 Series": [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-thinking-exp",
        "gemini-2.0-pro-exp",
    ],
    "Gemini 2.5 Series": [
        "gemini-2.5-pro-exp",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "Gemini 3 Series": [
        "gemini-3-pro",
        "gemini-3-deep-think",
    ],
    "Embedding Models": [
        "gemini-embedding-001",
    ],
    "Common/Stable Models": [
        "gemini-2.0-flash",  # Default as of Jan 2025
        "gemini-1.5-pro",    # May be deprecated
        "gemini-1.5-flash",  # May be deprecated
    ]
}

def show_known_models():
    """Display known Gemini model names."""
    print("=" * 60)
    print("Known Google Gemini Models")
    print("=" * 60)
    print()
    
    for category, models in KNOWN_MODELS.items():
        print(f"{category}:")
        for model in models:
            print(f"  • {model}")
        print()

def list_gemini_models_from_api():
    """Fetch and display models from the API."""
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if not api_key or api_key == "your_api_key_here":
        print("⚠️  API key not configured. Showing known models only.")
        print("   To see your account's available models, add your API key to .env file.")
        print()
        return False
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    print("=" * 60)
    print("Fetching Models from Google Gemini API")
    print("=" * 60)
    print(f"Endpoint: {base_url}")
    print()
    
    try:
        models = client.models.list()
        gemini_models = [model.id for model in models if "gemini" in model.id.lower()]
        
        if gemini_models:
            print("Available Model IDs from API:")
            print("-" * 60)
            for model_id in sorted(gemini_models):
                print(f"  • {model_id}")
            print()
            return True
        else:
            print("No Gemini models found in API response.")
            print()
            return False
    except Exception as e:
        print(f"❌ Could not retrieve models from API: {e}")
        print()
        return False

def main():
    """Main entry point."""
    # Always show known models
    show_known_models()
    
    # Try to fetch from API
    api_success = list_gemini_models_from_api()
    
    # Recommendations
    print("=" * 60)
    print("Recommendations")
    print("=" * 60)
    print()
    print("For document conversion, recommended models:")
    print("  • gemini-2.0-flash       - Fast, good quality (default)")
    print("  • gemini-2.5-flash        - Latest fast model")
    print("  • gemini-2.5-pro-exp      - Higher quality, slower")
    print("  • gemini-3-pro             - Best quality (if available)")
    print()
    print("Note: Model availability depends on your API access tier.")
    print("      Some models may require specific API access levels.")
    print()

if __name__ == "__main__":
    main()
