# Development Guide

## Project Structure

```
my-ai-robot/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── main_agent.py      # Main agent loop
│   ├── agent_tools.py     # Tool definitions (20 tools)
│   ├── config.py          # Configuration & API keys
│   └── model_loader.py    # Multi-model loader
├── docs/                   # Documentation
│   ├── SETUP.md           # Installation & setup
│   ├── ARCHITECTURE.md    # System architecture
│   └── DEVELOPMENT.md     # This file
├── tests/                  # Test files
│   └── test_mouse.py      # Mouse control tests
├── my-env/                # Virtual environment
├── run.py                 # Entry point script
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project & linting config
├── Makefile              # Development commands
└── README.md             # Main documentation
```

## Linting & Code Quality

This project uses **ruff** and **mypy** for code quality and type checking.

### Quick Commands

```bash
# Check for issues
make lint

# Auto-fix issues
make format

# Run type checking
make type-check

# Run all checks
make check
```

### Using Tools Directly

```bash
# Ruff - Linter
ruff check .                           # Check for issues
ruff check --fix .                     # Auto-fix safe issues
ruff format .                          # Format code

# MyPy - Type Checker
mypy src/main_agent.py src/agent_tools.py
```

### Configuration

Linting configuration is in `pyproject.toml`:
- **Line length**: 100 characters
- **Python version**: 3.9+
- **Rules enabled**: E/W (pycodestyle), F (pyflakes), I (isort), N (naming), UP (pyupgrade), B (bugbear), C4 (comprehensions), SIM (simplify)

### IDE Integration

#### VSCode
Install extensions:
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)

Add to `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  }
}
```

## Adding New Tools

To add a new tool to the agent:

1. **Define tool in `src/agent_tools.py`:**
```python
from langchain.tools import tool

@tool
def your_new_tool(param1: str, param2: int) -> str:
    """
    Brief description of what your tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    try:
        # Add safety checks
        if not is_safe(param1):
            return "Error: Unsafe parameter"
        
        # Your tool logic here
        result = do_something(param1, param2)
        
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

2. **Add safety checks if needed:**
```python
def is_safe_for_your_tool(value: str) -> bool:
    """Check if value is safe to use"""
    dangerous = ["rm -rf", "sudo", "shutdown"]
    return not any(d in value.lower() for d in dangerous)
```

3. **Import in `src/main_agent.py`:**
```python
from src.agent_tools import (
    # ... existing imports ...
    your_new_tool,
)
```

4. **Add to tools list:**
```python
tools = [
    # ... existing tools ...
    your_new_tool,
]
```

5. **Update system prompt if needed** to explain when/how to use the tool

## Testing

### Manual Testing
```bash
python run.py
```

Then test with various commands:
- Simple tasks: "Create a folder called test"
- Complex tasks: "Organize my Desktop by file type"
- Error cases: Try commands that should fail gracefully

### Unit Tests
```bash
# Run tests
python -m pytest tests/

# Run specific test
python tests/test_mouse.py
```

## Model Configuration

### Using Different Models

Edit `src/config.py`:

```python
# Change primary model
GROQ_MODEL = "llama-3.3-70b-versatile"

# Change fallback
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Change local model
LOCAL_MODEL = "llama3.1:8b"

# Change fallback order
FALLBACK_ORDER = ["groq", "gemini", "ollama"]
```

### Adding New Model Providers

1. Install provider package:
```bash
pip install langchain-{provider}
```

2. Add to `src/model_loader.py`:
```python
def _load_new_provider():
    """Load new provider model"""
    from langchain_newprovider import ChatNewProvider
    
    llm = ChatNewProvider(
        model="model-name",
        api_key=config.NEW_API_KEY,
    )
    return llm
```

3. Update `src/config.py` with API key and model info

4. Add to fallback order

## Debugging

### Enable Verbose Output

The agent already shows all tool calls and results. For more detail:

1. Add debug prints in `src/agent_tools.py`
2. Check memory file: `cat ~/.ai_robot_memory.json`
3. Use the built-in debug tools:
   - `take_screenshot()` - Capture screen
   - `get_screen_info()` - Get screen dimensions
   - `check_running_apps()` - List running apps

### Common Issues

**Import errors after moving files:**
- Make sure all imports use `from src.module import ...`
- Run from project root: `python run.py`

**Tool not being called:**
- Check system prompt includes mention of the tool
- Verify tool docstring is clear
- Test with explicit command: "Use the X tool to do Y"

**Model errors:**
- Check API keys in `src/config.py`
- Verify internet connection for cloud models
- Check Ollama is running: `ollama list`

## Memory System

Agent memories are stored at: `~/.ai_robot_memory.json`

Structure:
```json
{
  "preferences": ["user likes detailed reports", ...],
  "facts": ["desktop is at ~/Desktop", ...],
  "mistakes": ["don't use relative paths", ...],
  "successes": ["list→create→move→verify pattern works", ...]
}
```

### Managing Memory

```bash
# View memory
cat ~/.ai_robot_memory.json

# Backup memory
cp ~/.ai_robot_memory.json ~/.ai_memory_backup.json

# Clear memory (from within agent)
"Clear all memories"
```

## Contributing

1. **Format code before committing:**
```bash
make format
```

2. **Run all checks:**
```bash
make check
```

3. **Update documentation** if adding new features

4. **Test thoroughly** with various commands

## Best Practices

1. **Safety First**: Always add safety checks for destructive operations
2. **Clear Docstrings**: Tools need clear descriptions for AI to use them properly
3. **Error Handling**: Use try/except blocks and return descriptive errors
4. **Verification**: Tools that modify state should verify their actions
5. **Logging**: Return detailed success/failure messages
6. **Type Hints**: Use type hints for better code quality

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Ollama Models](https://ollama.com/library)
- [Groq API](https://console.groq.com/)
- [Google AI Studio](https://makersuite.google.com/)

