This is a formal Product Requirements Document (PRD) / Technical Specification. You can save this content as SPECIFICATION.md and pass it to an AI coding assistant (like Cursor, GitHub Copilot Workspace, or ChatGPT) to generate the exact codebase.

It is structured to enforce the "Senior Engineer" standards: modularity, type safety, and error handling.

Technical Specification: Docx-to-PDF Merge Pipeline
1. Project Overview
Goal: Create a Python-based automation pipeline that ingests a directory of Microsoft Word (.docx) documents, converts them to PDF, and merges them into a single "Master PDF." Key Requirement: The Master PDF must contain a nested Table of Contents (Bookmarks) corresponding to the filenames of the source documents for navigation.

2. Technical Stack & Constraints
Language: Python 3.9+

Conversion Engine: LibreOffice (Headless CLI)

Constraint: Must run via subprocess.

Alternative: If Windows environment is detected, allow for comtypes (optional, but prioritize LibreOffice for portability).

PDF Manipulation: pypdf

Reasoning: Native python implementation, excellent support for creating Outlines/Bookmarks.

Type Hinting: Strict typing module usage.

Logging: Standard logging library (no print statements in core logic).

3. Architecture Design
The system will be composed of three distinct modules to ensure separation of concerns.

Module A: File Ingestor (ingestor.py)
Responsibilities:

Scan a target directory.

Filter for valid .docx files (ignore ~$ temp files).

Sort the files alphanumerically to ensure page order consistency.

Return a list of strictly typed Path objects.

Module B: Conversion Engine (converter.py)
Responsibilities:

Accept a list of source paths and a temporary output directory.

Execute the conversion command.

Validation: Verify the output PDF exists and has a size > 0 bytes.

Error Handling: If one file fails, log the error and continue; do not crash the pipeline.

Module C: Assembly Engine (assembler.py)
Responsibilities:

Initialize a PdfWriter.

Iterate through the converted PDFs.

Logic - The Merge:

Open source PDF.

Get page count.

Append all pages to Writer.

Logic - The Bookmark: Insert an Outline Item pointing to the first page of the newly appended section. Title = Filename (sanitized).

Write the final merged file.

4. Interface Definitions (Pseudocode)
The AI/IDE should implement the following signatures:

Python
# converter.py
def batch_convert_to_pdf(source_files: List[Path], temp_dir: Path) -> List[Path]:
    """
    Converts docx to pdf using LibreOffice headless.
    Returns a list of successfully converted PDF paths.
    """
    pass

# assembler.py
def merge_pdfs_with_toc(pdf_files: List[Path], output_path: Path) -> None:
    """
    Merges PDFs and creates a bookmark for each file at its starting page.
    Metadata: Sets Title and Author.
    """
    pass

# main.py
def pipeline_orchestrator(input_dir: str, output_filename: str):
    """
    1. Setup temp dir.
    2. Get files.
    3. Convert.
    4. Merge.
    5. Cleanup temp dir (try/finally block).
    """
    pass
5. Functional Requirements
Cleanup: The system must use a tempfile.TemporaryDirectory or manually remove the staging folder in a finally block.

Concurrency (Optional): If the file count > 10, the converter should use concurrent.futures.ThreadPoolExecutor to parallelize LibreOffice calls.

Sanitization: Source filenames used in Bookmarks should have underscores replaced with spaces and extensions removed (e.g., 01_Project_Scope.docx -> "01 Project Scope").

6. Edge Case Handling
Empty Directory: Raise ValueError if no .docx files are found.

Corrupt File: If a file fails conversion, log it as ERROR and exclude it from the final merge. Do not let one bad file stop the process.

Locked Files: Handle PermissionError gracefully if a file is open in Word.

7. Testing Plan
Unit Test: Mock the subprocess.run to simulate conversion success/failure.

Integration Test: Run the pipeline on a folder with 3 dummy .docx files and verify the output PDF has exactly 3 bookmarks.