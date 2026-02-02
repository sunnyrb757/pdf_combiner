#!/usr/bin/env python3
"""
Example execution script template.

This demonstrates the structure for Layer 3 execution scripts.
Scripts should be deterministic, well-commented, and handle errors gracefully.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """
    Main execution function.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Your logic here
        print("Example script executed successfully")
        
        # Example: Read environment variable
        # api_key = os.getenv('EXAMPLE_API_KEY')
        # if not api_key:
        #     raise ValueError("EXAMPLE_API_KEY not found in environment")
        
        # Example: Work with .tmp directory
        tmp_dir = Path('.tmp')
        tmp_dir.mkdir(exist_ok=True)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
