from langchain.tools import tool
import pyautogui
import numpy as np
import random
import time
from scipy.interpolate import splprep, splev
import os
import subprocess

DANGEROUS_COMMANDS = ['rm -rf', 'sudo rm', 'format', 'delete system', 'shutdown -h']

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