#!/usr/bin/env python3
"""
Module A: File Ingestor (ingestor.py)
Responsibilities:
- Scan target directory for .docx files.
- Filter out temporary Word files (e.g., ~$file.docx).
- Sort files alphanumerically.
- Return list of Path objects.
"""

import os
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

def get_docx_files(input_dir: Path) -> List[Path]:
    """
    Scans a directory for .docx files and returns a sorted list of Path objects.
    
    Args:
        input_dir: The directory to scan.
        
    Returns:
        List[Path]: Sorted list of valid .docx files.
        
    Raises:
        ValueError: If no .docx files are found or directory doesn't exist.
    """
    if not input_dir.exists() or not input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {input_dir}")

    # Find .docx files, ignore temporary files starting with ~$
    docx_files = [
        p for p in input_dir.glob("*.docx") 
        if not p.name.startswith("~$")
    ]

    if not docx_files:
        raise ValueError(f"No valid .docx files found in {input_dir}")

    # Sort alphanumerically
    docx_files.sort(key=lambda x: x.name.lower())
    
    logger.info(f"Found {len(docx_files)} files in {input_dir}")
    return docx_files

if __name__ == "__main__":
    # Test block
    logging.basicConfig(level=logging.INFO)
    try:
        test_dir = Path(".")
        files = get_docx_files(test_dir)
        for f in files:
            print(f"File: {f}")
    except Exception as e:
        print(f"Error: {e}")
