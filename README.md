# AI OS Agent Project

This is a local AI agent that controls your computer's mouse, keyboard, files, and apps via natural language commands. It runs on Python and uses Ollama for the AI brain.

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

9. (Optional) For Windows/Linux tweaks:
   - In `agent_tools.py`, change `subprocess.run(['open', '-a', app_name])` to cross-platform code. Add at top: `import platform`
   - Then in `open_app` tool: