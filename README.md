# AI OS Agent Project

This is a local AI agent that controls your computer's mouse, keyboard, files, apps, and **executes any terminal command** via natural language. It runs on Python and uses Ollama for the AI brain.

## Key Features
- 🖱️ **Mouse & Keyboard Control**: Move, click, type with human-like movements
- 📂 **File Operations**: Search, create folders, manage files
- 🚀 **App Launcher**: Open any application
- 🌐 **Web Browser**: Open URLs automatically
- 💻 **Terminal Commands**: Execute ANY safe terminal command (mkdir, ls, python scripts, git, etc.)
- 🛡️ **Safety First**: Blocks dangerous commands (rm -rf, shutdown, etc.)

## Requirements
- Python 3.10+ (download from python.org)
- Ollama (download from ollama.com) – for the local AI model.
- A computer with GUI (works on Mac, Windows, Linux).
- For GUI control (mouse/clicks): Grant accessibility permissions.
  - Mac: System Settings > Privacy & Security > Accessibility > Enable Python/Terminal.
  - Windows: May need admin rights; no special settings usually.
  - Linux: Install `xdotool` or similar if pyautogui has issues.

## Setup Instructions
1. Clone or download this folder (my-ai-robot) to your computer.

2. Open Terminal (Mac/Linux) or Command Prompt/PowerShell (Windows).

3. Go to the folder: `cd path/to/my-ai-robot`

4. Create a virtual environment: `python -m venv my-env`

5. Activate it:
   - Mac/Linux: `source my-env/bin/activate`
   - Windows: `my-env\Scripts\activate`

6. Install dependencies: `pip install -r requirements.txt`

7. Install Ollama (if not done): Go to ollama.com, download and install for your OS.

8. Download the AI model: In Terminal/Command Prompt, run `ollama pull llama3.1:8b` (supports tool calling; ~4-5GB download).

9. Run the agent: `python main_agent.py`

10. Start commanding! Type things like:
    - "Move mouse to 500, 300 and click"
    - "Open Chrome"
    - "Create a folder called test_project"
    - "List all Python files in the current directory"
    - "Run git status"

## Example Commands

### Mouse & GUI Control
- "Move the mouse to coordinates 800, 400"
- "Click the left mouse button"
- "Double click at current position"

### File & Folder Operations
- "Create a new folder called my_project"
- "List all files in the current directory"
- "Search for config.json file"
- "Show me the contents of README.md"

### Application Control
- "Open Safari"
- "Launch Visual Studio Code"
- "Open the Calculator app"

### Terminal Commands (NEW!)
- "Create a folder called data"
- "List all Python files with ls *.py"
- "Check git status"
- "Run my python script with python my_script.py"
- "Show current directory with pwd"
- "Copy file.txt to backup/file.txt"

### Web Browsing
- "Open google.com"
- "Go to github.com"

## Safety Features
The agent blocks dangerous commands including:
- `rm -rf` (recursive delete)
- `sudo rm` (delete with admin rights)
- `shutdown`, `reboot`, `halt` (system power commands)
- `mkfs`, `dd` (disk formatting)
- `chmod -r 777 /` (permission changes)
- Fork bombs and other destructive commands

## How It Works
1. You type a natural language command
2. The AI (Llama 3.1) decides which tools to use
3. Tools execute safely with error handling
4. Results are shown with feedback
5. The agent remembers context for follow-up commands

## Troubleshooting
- **Mouse not moving?** Grant accessibility permissions (see Requirements)
- **Ollama not found?** Make sure Ollama is installed and running
- **Command blocked?** The safety filter is protecting you from dangerous commands
- **Tool errors?** Check the error message - it usually tells you what's wrong

Type `exit` to quit the agent.