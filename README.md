# 3-Layer Agent Architecture

This repository implements a 3-layer architecture for AI agent workflows, designed to maximize reliability by separating concerns between natural language instructions, intelligent routing, and deterministic execution.

## Architecture Overview

### Layer 1: Directives (What to do)
- **Location**: `directives/`
- **Purpose**: SOPs written in Markdown that define goals, inputs, tools, outputs, and edge cases
- **Format**: Natural language instructions, like you'd give a mid-level employee

### Layer 2: Orchestration (Decision making)
- **Purpose**: Intelligent routing by AI agents
- **Responsibilities**: Read directives, call execution tools in the right order, handle errors, ask for clarification, update directives with learnings
- **Key principle**: The glue between intent and execution

### Layer 3: Execution (Doing the work)
- **Location**: `execution/`
- **Purpose**: Deterministic Python scripts that handle API calls, data processing, file operations, and database interactions
- **Characteristics**: Reliable, testable, fast, well-commented

## Why This Works

AI agents are probabilistic, but business logic is deterministic. By pushing complexity into deterministic code:
- 90% accuracy per step becomes sustainable
- Errors don't compound
- The agent focuses on decision-making, not implementation details

## Directory Structure

```
.
├── AGENTS.md              # Architecture specification
├── directives/            # Layer 1: SOPs in Markdown
│   └── example_directive.md
├── execution/             # Layer 3: Python scripts
│   └── example_script.py
├── .tmp/                  # Temporary/intermediate files (not committed)
├── .env                   # Environment variables (not committed)
├── .env.template          # Template for environment setup
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Getting Started

### 1. Setup Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.template .env
# Edit .env with your API keys and credentials
```

### 2. Create a Directive

Create a new file in `directives/` following the template in `example_directive.md`. Define:
- Goal
- Inputs
- Tools/Scripts
- Process steps
- Outputs
- Edge cases

### 3. Create an Execution Script

Create a new Python script in `execution/` following the template in `example_script.py`. Make it:
- Deterministic
- Well-commented
- Error-handling
- Environment-aware (use `.env` for config)

### 4. Run with AI Agent

The AI agent will:
1. Read the directive
2. Gather inputs
3. Execute the script(s)
4. Handle errors and edge cases
5. Update the directive with learnings

## Operating Principles

### 1. Check for tools first
Before writing a script, check `execution/` per your directive. Only create new scripts if none exist.

### 2. Self-anneal when things break
- Read error messages and stack traces
- Fix the script and test again
- Update the directive with learnings (API limits, timing, edge cases)

### 3. Update directives as you learn
Directives are living documents. When you discover:
- API constraints
- Better approaches
- Common errors
- Timing expectations

Update the directive to make the system stronger.

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets, Google Slides, or other cloud-based outputs that the user can access
- **Intermediates**: Temporary files needed during processing (stored in `.tmp/`)

**Key principle:** Local files are only for processing. Deliverables live in cloud services where the user can access them. Everything in `.tmp/` can be deleted and regenerated.

## Self-Annealing Loop

When something breaks:
1. Fix it
2. Update the tool
3. Test the tool
4. Update directive to include new flow
5. System is now stronger

## Notes

- See `AGENTS.md` for the complete architecture specification
- All intermediate files go in `.tmp/` (never committed)
- Environment variables and credentials go in `.env` (never committed)
- Keep scripts deterministic and well-tested
- Update directives as you learn

---

**Be pragmatic. Be reliable. Self-anneal.**
