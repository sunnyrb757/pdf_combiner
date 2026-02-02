# Docx-to-PDF Merge Pipeline (3-Layer Architecture)

This tool automates the process of converting multiple Microsoft Word (.docx) documents into a single, merged "Master PDF" with a visual Table of Contents and sidebar bookmarks.

## Prerequisites

For your associate to run this codebase successfully, they will need the following environment:

1.  **Operating System**: Windows (required for MS Word automation).
2.  **Microsoft Word**: Must be installed and licensed.
3.  **Python 3.9+**: Installed and added to the PATH.
4.  **Dependencies**: Install the required libraries via `pip`.

## Getting Started

### 1. Setup Environment

```powershell
# Clone the repository
git clone https://github.com/sunnyrb757/pdf_combiner
cd pdf_combiner

# Create a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Pipeline

Place your `.docx` files in a folder (e.g., `Documents/`) and run the orchestrator:

```powershell
python execution/pipeline.py --input "path/to/your/docx_folder" --output "Master_Document.pdf"
```

## How it Works

The pipeline follows a 3-layer architecture:
-   **Ingestor**: Finds and sorts your Word files (ignoring temporary files).
-   **Converter**: Connects to MS Word to export each file as a high-fidelity PDF.
-   **Assembler**: Merges the PDFs, generates sidebar bookmarks, and creates a visual Table of Contents page at the start of the document.

## Notes
-   The tool uses **Microsoft Word** for conversion to ensure formatting matches exactly what you see in the app.
-   All intermediate files are stored in a temporary directory and cleaned up automatically.
-   If a file is open in Word, the script handles it gracefully but it is recommended to close Word before running for best results.
