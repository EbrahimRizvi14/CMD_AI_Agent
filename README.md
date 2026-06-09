# CMD AI Agent

CMD AI Agent is a Python-based command-line shell with built-in AI assistance. It supports common shell-style commands and adds AI-powered commands for explaining files, analyzing program output, summarizing the project, and answering short terminal-friendly questions.

## Features

- Interactive custom shell prompt
- Built-in commands for navigation and basic terminal actions
- AI chat command for quick command-line assistance
- AI file reader that explains source files
- AI run analyzer that executes Python files and summarizes results or errors
- AI project summarizer for Python source files in the workspace
- External command lookup through the system `PATH`

## Project Structure

```text
.
+-- terminal.py       # Main shell entry point
+-- testFile.py       # Small test file used for terminal behavior checks
+-- ai/
    +-- config.py     # System prompts used by the AI assistant
    +-- tools.py      # Groq API integration and AI command handlers
    +-- utils.py      # File-reading utility
```

## Requirements

- Python 3.10 or later
- A Groq API key
- Python packages:
  - `groq`
  - `python-dotenv`

## Setup

1. Clone or open the project directory.

2. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies.

   ```powershell
   pip install groq python-dotenv
   ```

4. Create a `.env` file in the project root and add your Groq API key.

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

Start the shell:

```powershell
python terminal.py
```

You will see an interactive prompt:

```text
$
```

### Built-in Commands

| Command | Description |
| --- | --- |
| `help` | Show available built-in commands |
| `pwd` | Print the current working directory |
| `cd <path>` | Change the current directory |
| `ls` | List visible files and folders in the current directory |
| `echo <text>` | Print text to the terminal |
| `type <command>` | Show whether a command is built in or available on `PATH` |
| `exit` | Exit the shell |

### AI Commands

| Command | Description |
| --- | --- |
| `ai <question>` | Ask the AI assistant a short question |
| `ai read <file>` | Explain a file and highlight obvious issues |
| `ai run <file>` | Run a Python file and analyze its output or error |
| `ai project` | Summarize the Python project structure and architecture |

Examples:

```text
ai What does this project do?
ai read terminal.py
ai run test.py
ai project
```

## How It Works

`terminal.py` runs the interactive shell loop, parses user input with `shlex`, handles built-in commands, and delegates AI commands to functions in `ai/tools.py`.

`ai/tools.py` loads the Groq client using `GROQ_API_KEY`, sends prompts to the `llama-3.3-70b-versatile` model, and formats responses for terminal use. Prompt behavior is defined in `ai/config.py`, while `ai/utils.py` provides a small helper for reading file contents.

## Notes

- `ai run <file>` currently executes Python files with `python <file>`.
- AI commands require a valid `GROQ_API_KEY` in the `.env` file.
- Hidden directories are skipped when listing files and summarizing the project.
