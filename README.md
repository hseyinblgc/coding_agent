# Coding Agent (LLM Tool-Calling Project)

A lightweight Python coding agent that uses OpenAI-compatible chat completions (via OpenRouter) and function/tool calling to inspect files, edit files, and execute Python scripts inside a constrained workspace.

## Overview

This repository combines:

- An LLM orchestration loop in `./main.py`
- A dynamic tool dispatcher in `./call_function.py`
- Secure local tools in `./functions/`
- A sample target workspace in `./calculator/`

The agent receives a prompt, decides when to call tools, executes them, and feeds tool results back to the model until a final answer is produced.

## Features

- **OpenAI function/tool calling infrastructure**  
  Registers tool schemas (`get_files_info`, `get_file_content`, `write_file`, `run_python_file`) and passes them to `chat.completions.create(...)`.

- **Loop-preventing iteration limits (multi-turn tool calling)**  
  Supports chained tool calls across turns with a hard stop (`for _ in range(20)`) to prevent infinite loops.

- **File I/O operations (reading/writing files)**  
  Includes guarded file readers/writers that enforce path boundaries to keep access within the permitted working directory.

- **Python code execution capabilities (`run_python_file`)**  
  Runs `.py` files with optional arguments, captures stdout/stderr, and enforces path and file-type safety checks.

## Repository Structure

```text
coding_agent/
├── main.py                     # LLM loop + tool-call orchestration
├── call_function.py            # Tool dispatcher and schema registry
├── prompts.py                  # System prompt for agent behavior
├── config.py                   # Shared limits/constants
├── functions/
│   ├── get_files_info.py       # Directory listing tool
│   ├── get_file_content.py     # File read/write tools
│   └── run_python_file.py      # Python execution tool
├── calculator/                 # Example project the agent can operate on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
└── test_*.py                   # Tool behavior demonstration scripts
```

## Commit History Snapshot

Current visible history shows two foundational milestones:

1. **`feat(functions): introduce utility to dynamically call tool functions`**  
   Initial project structure, tool implementations, and dynamic dispatch.
2. **`feat(llm): implement multi-turn tool calling with iteration limit`**  
   Added multi-step tool-call looping and maximum-iteration protection in `main.py`.

## Installation (Python `.venv`)

### 1) Clone and enter the project

```bash
git clone https://github.com/hseyinblgc/coding_agent.git
cd coding_agent
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> On Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`

### 3) Install dependencies

Using `uv` (lockfile is included):

```bash
uv sync
```

Or with `pip`:

```bash
pip install -U pip
pip install openai==2.44.0 python-dotenv==1.1.0
```

### 4) Configure environment variables

Create a `.env` file in the repository root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

Run the agent with a natural-language task:

```bash
python main.py "Inspect the calculator project, run its tests, and summarize any failures."
```

Verbose mode:

```bash
python main.py "List files and explain the project layout." --verbose
```

## Practical Scenario

Example workflow:

1. Ask the agent to inspect `/calculator` and identify entry points.
2. The model calls `get_files_info` and `get_file_content` to map the codebase.
3. The model calls `run_python_file` to execute `calculator/tests.py`.
4. If needed, it calls `write_file` to apply updates.
5. The loop continues until the model returns a final natural-language response (or reaches the iteration cap).

## Notes

- Python requirement is `>=3.13` (see `./pyproject.toml`).
- Tool execution is sandboxed to an injected working directory (`./calculator` in current dispatcher logic).