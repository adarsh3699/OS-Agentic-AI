# Setup Guide

## Requirements
- Python 3.10+ (download from python.org)
- Ollama (download from ollama.com) – for the local AI model
- A computer with GUI (works on Mac, Windows, Linux)
- For GUI control (mouse/clicks): Grant accessibility permissions
  - Mac: System Settings > Privacy & Security > Accessibility > Enable Python/Terminal
  - Windows: May need admin rights; no special settings usually
  - Linux: Install `xdotool` or similar if pyautogui has issues

## Installation

1. **Clone or download this folder** to your computer

2. **Navigate to the folder:**
```bash
cd path/to/my-ai-robot
```

3. **Create a virtual environment:**
```bash
python -m venv my-env
```

4. **Activate it:**
   - Mac/Linux: `source my-env/bin/activate`
   - Windows: `my-env\Scripts\activate`

5. **Install dependencies:**
```bash
pip install -r requirements.txt
```

6. **Install Ollama** (if not done): Go to ollama.com, download and install for your OS

7. **Download the AI model:**
```bash
ollama pull llama3.1:8b
```

## Multi-Model Setup (Recommended)

The agent supports 3 AI models with automatic fallback:

1. **Groq Llama 3.3 70B** (Primary) - Fastest, most powerful free model
2. **Google Gemini 2.0** (Fallback) - Reliable Google infrastructure
3. **Local Llama 3.1 8B** (Backup) - Offline capability

### Configure API Keys

Edit `src/config.py` and add your API keys:

```python
GROQ_API_KEY = "your_groq_api_key"      # Get from: console.groq.com
GEMINI_API_KEY = "your_gemini_api_key"  # Get from: makersuite.google.com
```

**Model Priority:**
```
1. Groq Llama 3.3 70B    ⚡⚡⚡⚡ ⭐⭐⭐⭐⭐  FREE (Primary)
2. Google Gemini 2.0     ⚡⚡⚡   ⭐⭐⭐⭐⭐  FREE (Fallback)
3. Local Llama 3.1 8B    ⚡⚡     ⭐⭐        FREE (Backup)
```

## Running the Agent

```bash
python run.py
```

Or directly:
```bash
python -m src.main_agent
```

## Example Commands

### Mouse & GUI Control
- "Move the mouse to coordinates 800, 400"
- "Click the left mouse button"
- "Double click at current position"

### File & Folder Operations
- "Create a new folder called my_project"
- "List all files in the current directory"
- "Search for config.json file"

### Application Control
- "Open Safari"
- "Launch Visual Studio Code"

### Terminal Commands
- "Create a folder called data"
- "List all Python files"
- "Check git status"
- "Show current directory"

### Web Browsing
- "Open google.com"
- "Go to github.com"

## Troubleshooting

- **Mouse not moving?** Grant accessibility permissions (see Requirements)
- **Ollama not found?** Make sure Ollama is installed and running
- **Command blocked?** The safety filter is protecting you from dangerous commands
- **Tool errors?** Check the error message - it usually tells you what's wrong
- **Groq failed?** Check API key in `src/config.py` and verify internet connection
- **Gemini failed?** Regenerate key at: https://makersuite.google.com

Type `exit` to quit the agent.

