# 🤖 AI Robot - Local Agentic AI Assistant

A powerful local AI agent that controls your computer through natural language. Move your mouse, type, manage files, run commands, and more - all through conversation with AI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## ✨ Key Features

- 🖱️ **Mouse & Keyboard Control** - Move, click, type with human-like movements
- 📂 **File Operations** - Search, create, manage files and folders
- 🚀 **App Launcher** - Open any application
- 💻 **Terminal Commands** - Execute safe terminal commands
- 🧠 **Self-Aware** - Critiques its own work, verifies results
- 💾 **Persistent Memory** - Learns from mistakes across sessions
- 🔄 **Error Recovery** - Tries 5+ alternatives when stuck
- 🛡️ **Safety First** - Blocks dangerous commands

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd my-ai-robot

# 2. Set up virtual environment
python -m venv my-env
source my-env/bin/activate  # On Windows: my-env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama (for local AI)
# Download from: https://ollama.com
ollama pull llama3.1:8b

# 5. Configure API keys (optional but recommended)
# Edit src/config.py and add your Groq/Gemini API keys

# 6. Run the agent
python run.py
```

## 🎯 Example Commands

```
"Create a folder called Projects on my Desktop"
"Organize my Desktop by file type"
"Open Visual Studio Code"
"Move all images to a new folder called Photos"
"Search for config.json file"
"List all Python files in current directory"
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Architecture](docs/ARCHITECTURE.md)** - How the system works
- **[Development](docs/DEVELOPMENT.md)** - Contributing and extending

## 🏗️ Project Structure

```
my-ai-robot/
├── src/                   # Source code
│   ├── main_agent.py     # Main agent loop
│   ├── agent_tools.py    # 20 tools for computer control
│   ├── config.py         # Configuration & API keys
│   └── model_loader.py   # Multi-model loader
├── docs/                  # Documentation
├── tests/                 # Test files
├── run.py                # Entry point
└── requirements.txt      # Dependencies
```

## 🤖 AI Models

The agent supports multiple AI providers with automatic fallback:

| Model | Type | Speed | Intelligence | Cost |
|-------|------|-------|--------------|------|
| **Groq Llama 3.3 70B** | Cloud | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | FREE |
| **Google Gemini 2.0** | Cloud | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | FREE |
| **Local Llama 3.1 8B** | Local | ⚡⚡ | ⭐⭐ | FREE |

**Recommended:** Add Groq and Gemini API keys in `src/config.py` for best performance.

## 🛠️ Available Tools (20 Total)

### Computer Control (8 tools)
- `move_mouse`, `click_mouse`, `type_text`, `press_key`
- `search_file`, `open_app`, `open_url`, `check_running_apps`

### File Operations (4 tools)
- `execute_terminal_command`, `get_current_directory`
- `read_file_content`, `list_directory`

### Professional Features (8 tools)
- `self_critique` - Self-evaluation before claiming done
- `verify_expectations` - Result verification
- `save_to_memory` / `recall_from_memory` - Persistent learning
- `debug_last_error` - Error recovery with alternatives
- `take_screenshot`, `get_screen_info` - Visual debugging

## 🛡️ Safety Features

The agent blocks dangerous commands automatically:
- `rm -rf` (recursive delete)
- `sudo rm` (force delete)  
- `shutdown`, `reboot`, `halt`
- `mkfs`, `format` (disk formatting)
- Fork bombs and system destructive commands

All commands have:
- ✅ 30-second timeout protection
- ✅ User-level permissions only
- ✅ Input sanitization
- ✅ Safe execution environment

## 💡 What Makes This "Agentic"?

| Feature | Traditional AI | This Agent |
|---------|---------------|------------|
| **Planning** | Executes single command | Breaks down complex tasks |
| **Error Handling** | Fails and reports | Debugs, tries alternatives |
| **Verification** | Assumes success | Verifies every action |
| **Learning** | No adaptation | Learns across sessions |
| **Autonomy** | Needs instructions | Takes initiative |

**~80% feature parity** with professional AI systems like Cursor AI and Devin!

## 🔧 Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run linting
make lint

# Auto-format code
make format

# Type checking
make type-check

# Run all checks
make check
```

See [Development Guide](docs/DEVELOPMENT.md) for more details.

## 📝 Memory System

The agent remembers things across sessions:
- User preferences and corrections
- Successful strategies
- Mistakes to avoid
- Important facts

Memory is stored at: `~/.ai_robot_memory.json`

## 🤝 Contributing

Contributions are welcome! Please:
1. Run `make format` before committing
2. Run `make check` to verify code quality
3. Update documentation for new features
4. Test thoroughly with various commands

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [LangChain](https://python.langchain.com/) - Agent framework
- [Ollama](https://ollama.com/) - Local AI runtime
- [Groq](https://groq.com/) - Fast cloud inference
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Google's AI

## 🆘 Support

- **Issues?** Check [Setup Guide](docs/SETUP.md) troubleshooting section
- **Questions?** See [Architecture](docs/ARCHITECTURE.md) for how it works
- **Want to extend?** Read [Development Guide](docs/DEVELOPMENT.md)

---

**Made with 🤖 by the AI Robot Team**

*"Give me a goal, I'll find the path"*
