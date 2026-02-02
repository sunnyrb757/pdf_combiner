#!/usr/bin/env python3
"""
Module B: Conversion Engine (converter.py)
Responsibilities:
- Convert .docx to PDF using Microsoft Word COM automation.
- Handle batch conversion.
- Validate output files.
"""

import os
import logging
import sys
from pathlib import Path
from typing import List
import time

# Attempt to import win32com
try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None

logger = logging.getLogger(__name__)

def convert_docx_to_pdf(docx_path: Path, output_dir: Path) -> Path:
    """
    Converts a single .docx file to PDF using MS Word.
    """
    if win32com is None:
        raise ImportError("pywin32 is not installed. Please install it using 'pip install pywin32'")

    # Ensure absolute paths for COM
    docx_path = docx_path.absolute()
    output_pdf_path = output_dir.absolute() / f"{docx_path.stem}.pdf"
    
    # Word ExportFormat constant for PDF
    wdExportFormatPDF = 17 
    
    word = None
    doc = None
    try:
        # Initialize COM in case of threading
        pythoncom.CoInitialize()
        
        # Connect to Word
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        
        logger.info(f"Converting {docx_path.name} to PDF...")
        
        # Open document
        doc = word.Documents.Open(str(docx_path), ReadOnly=True)
        
        # Export as PDF
        doc.ExportAsFixedFormat(str(output_pdf_path), wdExportFormatPDF)
        
        if not output_pdf_path.exists() or output_pdf_path.stat().st_size == 0:
            raise RuntimeError(f"Failed to create valid PDF for {docx_path}")
            
        return output_pdf_path
        
    except Exception as e:
        logger.error(f"Error converting {docx_path.name}: {e}")
        raise
    finally:
        if doc:
            doc.Close(0) # 0 = wdDoNotSaveChanges
        if word:
            word.Quit()
        pythoncom.CoUninitialize()

def batch_convert_to_pdf(source_files: List[Path], temp_dir: Path) -> List[Path]:
    """
    Converts a list of .docx files to PDF.
    """
    temp_dir.mkdir(parents=True, exist_ok=True)
    converted_pdfs = []
    
    for docx in source_files:
        try:
            pdf_path = convert_docx_to_pdf(docx, temp_dir)
            converted_pdfs.append(pdf_path)
        except Exception as e:
            logger.error(f"Skipping {docx.name} due to error: {e}")
            
    return converted_pdfs

if __name__ == "__main__":
    # Test snippet (requires Word and a file)
    logging.basicConfig(level=logging.INFO)
    print("This module is intended to be called by pipeline.py")
