from langchain.tools import tool
import pyautogui
import numpy as np
import random
import time
from scipy.interpolate import splprep, splev
import os
import subprocess

DANGEROUS_COMMANDS = [
    'rm -rf', 'sudo rm', 'format', 'delete system', 'shutdown -h',
    'mkfs', 'dd if=', ':(){:', 'fork bomb', '> /dev/sda',
    'mv /* ', 'chmod -r 777 /', 'killall', 'pkill',
    'halt', 'reboot', 'init 0', 'init 6', 'poweroff'
]

def is_safe(action):
    return all(danger.lower() not in action.lower() for danger in DANGEROUS_COMMANDS)

@tool
def move_mouse(x: int, y: int, human_like: bool = True):
    """Moves the mouse to x,y coordinates, optionally with human-like movement."""
    if not is_safe(f"move to {x},{y}"):
        return "Unsafe action blocked."
    try:
        current_x, current_y = pyautogui.position()
        if human_like:
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            points = np.array([[current_x, current_y], [current_x + (x - current_x)/2 + random.uniform(-50, 50), current_y + (y - current_y)/2], [x, y]])
            tck, u = splprep(points.T, s=0)
            u_new = np.linspace(0, 1, 20)
            path = splev(u_new, tck)
            for px, py in zip(*path):
                pyautogui.moveTo(px, py, duration=0.01)
                time.sleep(random.uniform(0.01, 0.05))
        else:
            pyautogui.moveTo(x, y)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {str(e)}. Try different coordinates or check permissions."

@tool
def click_mouse(button: str = 'left'):
    """Clicks the mouse (left/right/double)."""
    if not is_safe("click"):
        return "Unsafe action blocked."
    try:
        if button == 'left':
            pyautogui.click()
        elif button == 'right':
            pyautogui.rightClick()
        elif button == 'double':
            pyautogui.doubleClick()
        time.sleep(random.uniform(0.1, 0.3))
        return f"Clicked {button} button."
    except Exception as e:
        return f"Error clicking: {str(e)}. Maybe mouse is in a bad spot?"

@tool
def search_file(filename: str, start_dir: str = os.path.expanduser("~")):
    """Searches for a file starting from a directory."""
    if not is_safe(filename):
        return "Unsafe action blocked."
    try:
        matches = []
        for root, _, files in os.walk(start_dir):
            if filename in files:
                matches.append(os.path.join(root, filename))
        return matches or "File not found."
    except Exception as e:
        return f"Error searching file: {str(e)}. Check directory permissions."

@tool
def open_app(app_name: str):
    """Opens an app on Mac."""
    if not is_safe(app_name):
        return "Unsafe action blocked."
    try:
        subprocess.run(['open', '-a', app_name])
        return f"{app_name} opened."
    except Exception as e:
        return f"Error opening app: {str(e)}. Is the app installed?"

@tool
def open_url(url: str):
    """Opens a website URL in the default browser."""
    if not is_safe(url):
        return "Unsafe URL blocked."
    try:
        subprocess.run(['open', url])  # Mac command to open URLs
        return f"Opened {url} in browser."
    except Exception as e:
        return f"Error opening URL: {str(e)}. Is it a valid web address?"

@tool
def execute_terminal_command(command: str):
    """Executes any terminal command that is safe (not in DANGEROUS_COMMANDS list).
    Use this for any task like creating folders, listing files, running scripts, etc.
    Examples: 'mkdir new_folder', 'ls -la', 'pwd', 'cat file.txt', 'python script.py'
    """
    if not is_safe(command):
        return f"🚫 Unsafe command blocked: {command}. Contains dangerous keywords."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout for safety
        )
        output = result.stdout if result.stdout else result.stderr
        return_code = result.returncode
        
        if return_code == 0:
            return f"✅ Command executed successfully:\n{output if output else 'Command completed with no output.'}"
        else:
            return f"⚠️ Command failed with exit code {return_code}:\n{output}"
    except subprocess.TimeoutExpired:
        return "⏱️ Command timed out after 30 seconds. Use a different approach for long-running tasks."
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

@tool
def take_screenshot(filename: str = "debug_screenshot.png"):
    """Takes a screenshot for debugging. Useful to verify UI state or check what's on screen.
    Returns the path where screenshot was saved."""
    try:
        screenshot = pyautogui.screenshot()
        filepath = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        screenshot.save(filepath)
        return f"📸 Screenshot saved to: {filepath}"
    except Exception as e:
        return f"❌ Failed to take screenshot: {str(e)}"

@tool
def get_screen_info():
    """Gets screen dimensions and current mouse position. Useful for planning mouse movements."""
    try:
        screen_width, screen_height = pyautogui.size()
        mouse_x, mouse_y = pyautogui.position()
        return f"🖥️ Screen: {screen_width}x{screen_height} | Mouse position: ({mouse_x}, {mouse_y})"
    except Exception as e:
        return f"❌ Error getting screen info: {str(e)}"

@tool
def check_running_apps():
    """Lists currently running applications. Useful to verify if an app is already open before trying to open it."""
    try:
        result = subprocess.run(
            "ps aux | grep -i '.app/Contents/MacOS' | grep -v grep | awk '{print $11}' | sed 's|.*/||' | sort -u",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        apps = result.stdout.strip()
        if apps:
            return f"🔍 Running apps:\n{apps}"
        else:
            return "No apps detected or error reading process list."
    except Exception as e:
        return f"❌ Error checking apps: {str(e)}"

@tool
def type_text(text: str, interval: float = 0.05):
    """Types text at current cursor position. Useful for filling forms, writing documents, etc.
    interval: time between each keystroke (default 0.05s)."""
    if not is_safe(text):
        return "🚫 Unsafe text blocked."
    try:
        pyautogui.write(text, interval=interval)
        return f"⌨️ Typed: '{text[:50]}{'...' if len(text) > 50 else ''}'"
    except Exception as e:
        return f"❌ Error typing text: {str(e)}"

@tool
def press_key(key: str, times: int = 1):
    """Presses a keyboard key. Examples: 'enter', 'tab', 'escape', 'backspace', 'command', 'space'.
    Can press multiple times. Useful for keyboard shortcuts and navigation."""
    if not is_safe(key):
        return "🚫 Unsafe key blocked."
    try:
        for _ in range(times):
            pyautogui.press(key)
            time.sleep(0.1)
        return f"⌨️ Pressed '{key}' {times} time(s)"
    except Exception as e:
        return f"❌ Error pressing key: {str(e)}. Valid keys: enter, tab, escape, space, command, etc."

@tool
def get_current_directory():
    """Gets the current working directory. Useful for file operations and understanding context."""
    try:
        cwd = os.getcwd()
        return f"📁 Current directory: {cwd}"
    except Exception as e:
        return f"❌ Error getting directory: {str(e)}"

@tool
def read_file_content(filepath: str, max_lines: int = 50):
    """Reads content from a file. Useful for debugging, checking configurations, or reading data.
    max_lines: maximum number of lines to read (default 50 to avoid overwhelming output)."""
    if not is_safe(filepath):
        return "🚫 Unsafe file path blocked."
    try:
        with open(os.path.expanduser(filepath), 'r') as f:
            lines = f.readlines()[:max_lines]
            content = ''.join(lines)
            truncated = " (truncated)" if len(f.readlines()) > max_lines else ""
            return f"📄 Content of {filepath}{truncated}:\n{content}"
    except FileNotFoundError:
        return f"❌ File not found: {filepath}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"