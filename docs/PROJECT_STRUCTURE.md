# Project Structure

This document describes the organization of the AI Robot codebase.

## Directory Layout

```
my-ai-robot/
├── src/                        # Source code (Python package)
│   ├── __init__.py            # Package initialization
│   ├── main_agent.py          # Main agent loop and system prompt
│   ├── agent_tools.py         # 20 tool definitions
│   ├── config.py              # Configuration & API keys (gitignored)
│   ├── config.example.py      # Template for config.py
│   └── model_loader.py        # Multi-model loader with fallback
│
├── docs/                       # Documentation
│   ├── SETUP.md               # Installation & setup guide
│   ├── ARCHITECTURE.md        # System architecture & design
│   ├── DEVELOPMENT.md         # Developer guide
│   └── PROJECT_STRUCTURE.md   # This file
│
├── tests/                      # Test files
│   ├── __init__.py            # Test package
│   └── test_mouse.py          # Mouse control tests
│
├── my-env/                     # Virtual environment (gitignored)
│
├── run.py                      # Entry point script
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata & linting config
├── Makefile                   # Development commands
├── .gitignore                 # Git ignore rules
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT License
└── README.md                  # Main documentation
```

## Core Components

### `src/main_agent.py`
**Purpose:** Main event loop and agent orchestration

**Key Features:**
- System prompt definition (simplified for reliability)
- ReAct agent initialization
- User input handling with prompt_toolkit
- Tool orchestration
- Memory management

**Entry Point:**
```python
def main():
    """Main function to run the AI agent"""
```

### `src/agent_tools.py`
**Purpose:** 20 tools for computer control and AI capabilities

**Tool Categories:**
1. **Computer Control (8 tools)**
   - `move_mouse()`, `click_mouse()`, `type_text()`, `press_key()`
   - `search_file()`, `open_app()`, `open_url()`, `check_running_apps()`

2. **File Operations (4 tools)**
   - `execute_terminal_command()` - Run shell commands safely
   - `get_current_directory()` - Get working directory
   - `read_file_content()` - Read files
   - `list_directory()` - List directory contents with details

3. **Professional Features (8 tools)**
   - `self_critique()` - Self-evaluation
   - `verify_expectations()` - Result verification
   - `save_to_memory()` / `recall_from_memory()` / `clear_memory()` - Persistent learning
   - `debug_last_error()` - Error recovery
   - `take_screenshot()` / `get_screen_info()` - Visual debugging

**Safety:**
- `DANGEROUS_COMMANDS` list blocks destructive operations
- `is_safe()` function validates commands
- All tools have try/except error handling

### `src/model_loader.py`
**Purpose:** Load AI models with automatic fallback

**Fallback Order:**
1. Groq Llama 3.3 70B (Primary - fast, powerful)
2. Google Gemini 2.0 (Fallback - reliable)
3. Local Ollama (Backup - offline)

**Functions:**
- `get_model()` - Main function, tries providers in order
- `_load_groq()`, `_load_gemini()`, `_load_ollama()` - Provider-specific loaders

### `src/config.py`
**Purpose:** Configuration and API keys

**⚠️ Important:** This file is gitignored to protect API keys!

**Contents:**
- `GROQ_API_KEY`, `GEMINI_API_KEY` - API credentials
- `GROQ_MODEL`, `GEMINI_MODEL`, `LOCAL_MODEL` - Model selections
- `FALLBACK_ORDER` - Provider priority
- `MODEL_INFO` - Model capabilities and metadata

**Setup:** Copy `config.example.py` to `config.py` and add your keys.

## Running the Project

### From Root Directory
```bash
python run.py
```

### Direct Module Execution
```bash
python -m src.main_agent
```

### With Make
```bash
make run
```

## Development Workflow

### Before Committing
```bash
make format      # Auto-format code
make check       # Run linting + type checking
```

### Running Tests
```bash
make test        # Run all tests
python tests/test_mouse.py  # Run specific test
```

### Cleaning Up
```bash
make clean       # Remove cache files
```

## Configuration Files

### `pyproject.toml`
- Project metadata
- Ruff linter configuration
- MyPy type checker settings
- Line length: 100 characters
- Python version: 3.9+

### `requirements.txt`
Python dependencies:
- **LangChain** - Agent framework
- **LangGraph** - Agent orchestration
- **Model Providers** - langchain-ollama, langchain-groq, langchain-google-genai
- **UI** - prompt-toolkit
- **Computer Control** - pyautogui, pynput
- **Development** - ruff, mypy, pytest

### `Makefile`
Development commands:
- `make help` - Show all commands
- `make install` - Install dependencies
- `make run` - Run the agent
- `make lint` - Check code quality
- `make format` - Auto-format code
- `make type-check` - Type checking
- `make check` - All checks
- `make test` - Run tests
- `make clean` - Clean cache

### `.gitignore`
Ignores:
- Virtual environments (`my-env/`, `venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- API keys (`src/config.py`)
- User data (`.ai_robot_memory.json`)
- IDE files (`.vscode/`, `.idea/`)
- System files (`.DS_Store`)

## Memory System

### Location
`~/.ai_robot_memory.json`

### Structure
```json
{
  "preferences": ["user corrections", "preferred patterns"],
  "facts": ["important information"],
  "mistakes": ["errors to avoid"],
  "successes": ["strategies that worked"]
}
```

### Management
- Created automatically on first save
- Persists across sessions
- Can be cleared with `clear_memory()` tool
- Backup recommended: `cp ~/.ai_robot_memory.json ~/.ai_memory_backup.json`

## Import Structure

All imports use the `src` package:

```python
# In run.py
from src.main_agent import main

# In main_agent.py
from src.agent_tools import move_mouse, click_mouse, ...
from src.model_loader import get_model
from src import config

# In model_loader.py
from src import config
```

## Adding New Components

### New Tool
1. Add function in `src/agent_tools.py` with `@tool` decorator
2. Import in `src/main_agent.py`
3. Add to `tools` list
4. Update system prompt if needed

### New Model Provider
1. Install provider: `pip install langchain-{provider}`
2. Add loader function in `src/model_loader.py`
3. Add config in `src/config.py`
4. Add to `FALLBACK_ORDER`

### New Documentation
Add to `docs/` directory:
- Keep focused on single topic
- Use markdown format
- Link from main README.md

## Design Principles

1. **Separation of Concerns**
   - Source code in `src/`
   - Documentation in `docs/`
   - Tests in `tests/`
   - Config at root level

2. **Safety First**
   - API keys not in version control
   - Dangerous commands blocked
   - Error handling everywhere

3. **Developer Experience**
   - Simple entry point (`run.py`)
   - Clear documentation
   - Easy-to-use Makefile commands
   - Type hints for IDE support

4. **Modularity**
   - Tools are independent functions
   - Models are swappable
   - Configuration is external

5. **Professional Structure**
   - Standard Python package layout
   - Proper gitignore
   - Linting and type checking
   - Clear documentation

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for version history.

## License

MIT License - See [LICENSE](../LICENSE) for details.

