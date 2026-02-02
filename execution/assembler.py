#!/usr/bin/env python3
"""
Module C: Assembly Engine (assembler.py)
Responsibilities:
- Merge multiple PDFs into one.
- Add bookmarks based on original filenames.
- Set PDF metadata.
"""

import logging
from pathlib import Path
from typing import List
from pypdf import PdfWriter

logger = logging.getLogger(__name__)

def sanitize_bookmark_name(filename: str) -> str:
    """
    Sanitizes filename for use as a bookmark title.
    Example: 01_Project_Scope.pdf -> "01 Project Scope"
    """
    stem = Path(filename).stem
    return stem.replace("_", " ").strip()

def merge_pdfs_with_toc(pdf_files: List[Path], output_path: Path) -> None:
    """
    Merges PDFs and creates a bookmark for each file at its starting page.
    """
    if not pdf_files:
        raise ValueError("No PDF files provided for merging")

    writer = PdfWriter()
    current_page = 0

    for pdf_path in pdf_files:
        try:
            logger.info(f"Merging {pdf_path.name}...")
            
            # Use append to add pages and track count
            # We add a bookmark at the start page of this appended file
            bookmark_title = sanitize_bookmark_name(pdf_path.name)
            
            # Read input pdf
            writer.append(pdf_path)
            
            # Add bookmark
            # Note: writer.append appends the pages. We need to know where we started.
            writer.add_outline_item(bookmark_title, current_page)
            
            # Update page offset
            # writer.pages is a list of all pages in the writer
            current_page = len(writer.pages)
            
        except Exception as e:
            logger.error(f"Failed to merge {pdf_path.name}: {e}")
            raise

    # Set metadata
    writer.add_metadata({
        "/Title": "Master PDF Document",
        "/Producer": "3-Layer Docx-to-PDF Pipeline",
        "/Author": "Automated Agent"
    })

    # Write final file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)
    
    logger.info(f"Successfully created Master PDF at: {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("This module is intended to be called by pipeline.py")
