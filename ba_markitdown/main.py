#!/usr/bin/env python3
"""
BA MarkItDown - Convert documents to LLM-optimized Markdown.

This script converts various file formats (PDF, Word, Excel, images, etc.)
to clean, structured Markdown using the MarkItDown library and an LLM
for intelligent formatting and cleanup.
"""

import warnings
import os
import sys
import logging
import argparse
import json
from datetime import datetime
from pathlib import Path

# Suppress warnings before imports
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

from markitdown import MarkItDown
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from bot-level .env
# This allows unified configuration across all bot components
_env_path = Path(__file__).parent.parent / '.env'
load_dotenv(_env_path)

# Suppress noisy loggers
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)

# Exit codes for different error types
EXIT_SUCCESS = 0
EXIT_ENV_ERROR = 1
EXIT_FILE_NOT_FOUND = 2
EXIT_CONVERSION_ERROR = 3
EXIT_CLEANUP_ERROR = 4
EXIT_FFMPEG_MISSING = 5
EXIT_PERMISSION_ERROR = 6
EXIT_UNKNOWN_ERROR = 99

# Error messages mapping for structured output
ERROR_TYPES = {
    "ffmpeg": {
        "patterns": ["ffmpeg", "ffprobe", "audio", "video"],
        "exit_code": EXIT_FFMPEG_MISSING,
        "friendly": "This file requires ffmpeg for audio/video processing, which isn't installed.",
        "technical": None,  # Will be filled with actual error
        "suggestion": "For audio/video files, ffmpeg needs to be available on your system."
    },
    "permission": {
        "patterns": ["permission denied", "access denied", "cannot access"],
        "exit_code": EXIT_PERMISSION_ERROR,
        "friendly": "I don't have permission to access this file.",
        "technical": None,
        "suggestion": "Check that the file isn't open in another program and that you have read access."
    },
    "corrupt": {
        "patterns": ["corrupt", "invalid", "malformed", "damaged", "cannot read"],
        "exit_code": EXIT_CONVERSION_ERROR,
        "friendly": "This file appears to be corrupted or in an unsupported format.",
        "technical": None,
        "suggestion": "Try opening the file in its native application to verify it's not damaged."
    },
    "password": {
        "patterns": ["password", "encrypted", "protected"],
        "exit_code": EXIT_CONVERSION_ERROR,
        "friendly": "This file is password-protected.",
        "technical": None,
        "suggestion": "Please provide an unprotected version of the file."
    }
}


def classify_error(error_message: str) -> dict:
    """Classify an error message and return structured error info."""
    error_lower = error_message.lower()
    
    for error_type, info in ERROR_TYPES.items():
        for pattern in info["patterns"]:
            if pattern in error_lower:
                return {
                    "type": error_type,
                    "exit_code": info["exit_code"],
                    "friendly": info["friendly"],
                    "technical": error_message,
                    "suggestion": info["suggestion"]
                }
    
    # Default unknown error
    return {
        "type": "unknown",
        "exit_code": EXIT_UNKNOWN_ERROR,
        "friendly": "Something went wrong during conversion.",
        "technical": error_message,
        "suggestion": "You can try again or skip this file."
    }


def generate_frontmatter(input_file: str, output_file: str, organization: str = None, cleaned: bool = False) -> str:
    """Generate YAML frontmatter for tracking converted files."""
    input_path = Path(input_file)
    
    frontmatter = {
        "ba_markitdown": {
            "source_file": input_path.name,
            "source_path": str(input_path),
            "converted_at": datetime.now().isoformat(),
            "organization": organization or "unfiled",
            "cleaned": cleaned
        }
    }
    
    # Format as YAML
    lines = ["---"]
    lines.append("ba_markitdown:")
    for key, value in frontmatter["ba_markitdown"].items():
        if isinstance(value, bool):
            lines.append(f"  {key}: {'true' if value else 'false'}")
        else:
            lines.append(f"  {key}: {value}")
    lines.append("---")
    lines.append("")  # Empty line after frontmatter
    
    return "\n".join(lines)


def cleanup_markdown(client: OpenAI, model: str, content: str, filename: str) -> str:
    """
    Use LLM to clean up the converted markdown content.
    Removes garbage values, fixes formatting, optimizes for LLM consumption.
    """
    cleanup_prompt = f"""You are a document cleanup assistant. Your task is to clean up the following markdown content that was converted from a file called "{filename}".

Please:
1. Remove any garbage characters, OCR artifacts, or nonsensical text
2. Fix broken tables and formatting
3. Remove excessive whitespace while preserving document structure
4. Keep all meaningful content intact - do not summarize or remove real information
5. Ensure headings, lists, and other markdown elements are properly formatted
6. If there are obvious encoding issues, fix them
7. Preserve any code blocks, formulas, or technical notation

IMPORTANT: 
- Only remove clearly nonsensical content (random characters, broken encoding)
- Do NOT remove content just because it seems unusual - business documents often have specialized terminology
- Maintain the original document structure and hierarchy
- Return ONLY the cleaned markdown content, no explanations

Here is the content to clean:

{content}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise document cleanup assistant. Clean the markdown while preserving all meaningful content."},
                {"role": "user", "content": cleanup_prompt}
            ],
            temperature=0.1  # Low temperature for consistent, conservative cleanup
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Warning: Cleanup pass failed ({e}), using original content", file=sys.stderr)
        return content


def convert_file(input_file: str, output_file: str, cleanup: bool = False, 
                 frontmatter: bool = False, organization: str = None,
                 json_output: bool = False) -> int:
    """
    Convert a file to markdown.
    
    Returns exit code indicating success or type of failure.
    """
    result_data = {
        "success": False,
        "input_file": input_file,
        "output_file": output_file,
        "error": None
    }
    
    # Check environment variables
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    llm_model = os.getenv("LLM_MODEL")
    
    if not api_key:
        error_info = {
            "type": "env_error",
            "exit_code": EXIT_ENV_ERROR,
            "friendly": "API key is not configured.",
            "technical": "API_KEY environment variable is not set",
            "suggestion": "Please run setup and configure your .env file with your API key."
        }
        result_data["error"] = error_info
        if json_output:
            print(json.dumps(result_data, indent=2))
        else:
            print(f"Error: {error_info['friendly']}")
            print(f"Suggestion: {error_info['suggestion']}")
        return EXIT_ENV_ERROR
    
    if not base_url:
        error_info = {
            "type": "env_error",
            "exit_code": EXIT_ENV_ERROR,
            "friendly": "API base URL is not configured.",
            "technical": "BASE_URL environment variable is not set",
            "suggestion": "Please check your .env file has the BASE_URL configured."
        }
        result_data["error"] = error_info
        if json_output:
            print(json.dumps(result_data, indent=2))
        else:
            print(f"Error: {error_info['friendly']}")
            print(f"Suggestion: {error_info['suggestion']}")
        return EXIT_ENV_ERROR
    
    # Check input file exists
    if not os.path.exists(input_file):
        error_info = {
            "type": "file_not_found",
            "exit_code": EXIT_FILE_NOT_FOUND,
            "friendly": f"Could not find the file '{input_file}'.",
            "technical": f"File not found: {input_file}",
            "suggestion": "Please check the file path and try again."
        }
        result_data["error"] = error_info
        if json_output:
            print(json.dumps(result_data, indent=2))
        else:
            print(f"Error: {error_info['friendly']}")
            print(f"Suggestion: {error_info['suggestion']}")
        return EXIT_FILE_NOT_FOUND
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # Initialize MarkItDown
    md = MarkItDown(llm_client=client, llm_model=llm_model)
    
    if not json_output:
        print(f"Converting: {input_file}")
        print("Please note that large files might take a while...")
    
    try:
        # Perform conversion
        result = md.convert(input_file)
        content = result.text_content
        
        # Optional cleanup pass
        cleaned = False
        if cleanup and content:
            if not json_output:
                print("Running cleanup pass...")
            content = cleanup_markdown(client, llm_model, content, os.path.basename(input_file))
            cleaned = True
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write output with optional frontmatter
        with open(output_file, "w", encoding="utf-8") as f:
            if frontmatter:
                f.write(generate_frontmatter(input_file, output_file, organization, cleaned))
            f.write(content)
        
        result_data["success"] = True
        result_data["cleaned"] = cleaned
        
        if json_output:
            print(json.dumps(result_data, indent=2))
        else:
            print(f"Successfully created: {output_file}")
        
        return EXIT_SUCCESS
        
    except Exception as e:
        error_str = str(e)
        error_info = classify_error(error_str)
        result_data["error"] = error_info
        
        if json_output:
            print(json.dumps(result_data, indent=2))
        else:
            print(f"\nError: {error_info['friendly']}")
            print(f"Suggestion: {error_info['suggestion']}")
            print(f"\nTechnical details: {error_info['technical']}")
        
        return error_info["exit_code"]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert any file to Markdown using MarkItDown and your configured LLM.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py document.pdf output.md
  python main.py report.xlsx report.md --cleanup
  python main.py ../folder1/document.docx ../folder1_reference_md/document.md --frontmatter --organization "folder1_reference_md"
        """
    )
    
    # Required arguments
    parser.add_argument("input_file", help="Path to the file you want to convert")
    parser.add_argument("output_file", help="Path where you want to save the .md file")
    
    # Optional arguments
    parser.add_argument(
        "--cleanup", "-c",
        action="store_true",
        help="Run LLM cleanup pass to remove garbage and optimize formatting"
    )
    parser.add_argument(
        "--frontmatter", "-f",
        action="store_true",
        help="Add YAML frontmatter with tracking metadata"
    )
    parser.add_argument(
        "--organization", "-o",
        type=str,
        default=None,
        help="Organization/folder info for frontmatter (e.g., 'by_project/Alpha')"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON for programmatic parsing"
    )
    
    args = parser.parse_args()
    
    exit_code = convert_file(
        input_file=args.input_file,
        output_file=args.output_file,
        cleanup=args.cleanup,
        frontmatter=args.frontmatter,
        organization=args.organization,
        json_output=args.json
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
