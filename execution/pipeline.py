#!/usr/bin/env python3
"""
Orchestration Layer (pipeline.py)
Responsibilities:
- Glue the ingestor, converter, and assembler together.
- Setup temporary directories for intermediate files.
- Command-line interface for the user.
"""

import argparse
import logging
import sys
import tempfile
from pathlib import Path

# Add project root to path to allow absolute imports if running from root
sys.path.append(str(Path(__file__).parent.parent))

from execution.ingestor import get_docx_files
from execution.converter import batch_convert_to_pdf
from execution.assembler import merge_pdfs_with_toc

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def pipeline_orchestrator(input_dir_str: str, output_filename_str: str):
    """
    1. Setup temp dir.
    2. Get files.
    3. Convert.
    4. Merge.
    5. Cleanup temp dir (handled by TemporaryDirectory context).
    """
    logger = logging.getLogger("Pipeline")
    
    input_dir = Path(input_dir_str)
    output_path = Path(output_filename_str)
    
    try:
        # 1. Ingest
        docx_files = get_docx_files(input_dir)
        
        # 2. Setup temporary directory for intermediate PDFs
        # Using a context manager ensures cleanup even if steps fail
        with tempfile.TemporaryDirectory(dir=".tmp" if Path(".tmp").exists() else None) as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            logger.info(f"Using staging directory: {temp_dir}")
            
            # 3. Convert
            logger.info("Step: Conversion Starting")
            converted_pdfs = batch_convert_to_pdf(docx_files, temp_dir)
            
            if not converted_pdfs:
                logger.error("No files were successfully converted. Exiting.")
                return 1
            
            if len(converted_pdfs) < len(docx_files):
                logger.warning(f"Only {len(converted_pdfs)}/{len(docx_files)} files converted successfully.")
            
            # 4. Assemble
            logger.info("Step: Assembly Starting")
            merge_pdfs_with_toc(converted_pdfs, output_path)
            
            logger.info("Pipeline completed successfully.")
            return 0

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Docx-to-PDF Merge Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Directory containing .docx files")
    parser.add_argument("--output", "-o", default="master.pdf", help="Output filename for the merged PDF")
    
    args = parser.parse_args()
    
    setup_logging()
    sys.exit(pipeline_orchestrator(args.input, args.output))

if __name__ == "__main__":
    main()
