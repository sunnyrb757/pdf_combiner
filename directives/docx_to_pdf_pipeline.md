# Docx-to-PDF Pipeline Directive

## Goal
Automate the conversion of multiple `.docx` files into a single merged "Master PDF" with a navigation-ready Table of Contents (Bookmarks).

## Inputs
- **Input Directory**: Path containing the source `.docx` files.
- **Output Path**: Target path for the merged Master PDF.

## Tools/Scripts
- `execution/ingestor.py`: Scans and sorts source files.
- `execution/converter.py`: Converts `.docx` to PDF via MS Word COM.
- `execution/assembler.py`: Merges PDFs and adds bookmarks.
- `execution/pipeline.py`: Orchestrates the full workflow.

## Process
1. **Ingest**: Scan the input directory for `.docx` files, ignoring temporary Word files (starting with `~$`). Sort them alphanumerically.
2. **Convert**: For each `.docx` file, use Microsoft Word (headless) to export it as a high-quality PDF to a temporary directory.
3. **Assemble**:
    - Iterate through the converted PDFs in the sorted order.
    - Append each PDF's pages to a master writer.
    - Create a bookmark at the start of each appended section, using the sanitized filename (no extension, underscores replaced with spaces).
4. **Cleanup**: Delete all temporary intermediate PDF files.

## Outputs
- **Master PDF**: A single merged document with functional bookmarks.

## Edge Cases
- **No Docx Found**: Script should exit gracefully with a clear error message.
- **Conversion Failure**: If a specific file fails, log the error but continue with the remaining files.
- **Locked Files**: If a file is currently open in Word, the conversion might fail or use a cached version; the script should handle COM exceptions.

## Notes
- Requires Microsoft Word installed on the system (Windows only).
- Uses `pypdf` for low-level PDF manipulation to ensure bookmarks are correctly nested.
