import json
import os
import random
import subprocess
import time
from datetime import datetime

import numpy as np
import pyautogui
from langchain.tools import tool
from scipy.interpolate import splev, splprep

DANGEROUS_COMMANDS = [
    "rm -rf",
    "sudo rm",
    "format",
    "delete system",
    "shutdown -h",
    "mkfs",
    "dd if=",
    ":(){:",
    "fork bomb",
    "> /dev/sda",
    "mv /* ",
    "chmod -r 777 /",
    "killall",
    "pkill",
    "halt",
    "reboot",
    "init 0",
    "init 6",
    "poweroff",
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
            # Add slight randomness to make it more natural
            target_x = x + random.uniform(-5, 5)
            target_y = y + random.uniform(-5, 5)

            # Create more points for smooth curve (need at least 4 for cubic spline)
            points = np.array(
                [
                    [current_x, current_y],
                    [
                        current_x + (target_x - current_x) * 0.3 + random.uniform(-30, 30),
                        current_y + (target_y - current_y) * 0.3 + random.uniform(-20, 20),
                    ],
                    [
                        current_x + (target_x - current_x) * 0.7 + random.uniform(-20, 20),
                        current_y + (target_y - current_y) * 0.7 + random.uniform(-10, 10),
                    ],
                    [target_x, target_y],
                ]
            )
            # Use k=2 (quadratic) for more stability with fewer points
            tck, u = splprep(points.T, s=0, k=2)
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
def click_mouse(button: str = "left"):
    """Clicks the mouse (left/right/double)."""
    if not is_safe("click"):
        return "Unsafe action blocked."
    try:
        if button == "left":
            pyautogui.click()
        elif button == "right":
            pyautogui.rightClick()
        elif button == "double":
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
        subprocess.run(["open", "-a", app_name])
        return f"{app_name} opened."
    except Exception as e:
        return f"Error opening app: {str(e)}. Is the app installed?"


@tool
def open_url(url: str):
    """Opens a website URL in the default browser."""
    if not is_safe(url):
        return "Unsafe URL blocked."
    try:
        subprocess.run(["open", url])  # Mac command to open URLs
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
            timeout=30,  # 30 second timeout for safety
        )
        output = result.stdout if result.stdout else result.stderr
        return_code = result.returncode

        if return_code == 0:
            return f"✅ Command executed successfully:\n{output if output else 'Command completed with no output.'}"
        else:
            return f"⚠️ Command failed with exit code {return_code}:\n{output}"
    except subprocess.TimeoutExpired:
        return (
            "⏱️ Command timed out after 30 seconds. Use a different approach for long-running tasks."
        )
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
            timeout=5,
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
        return (
            f"❌ Error pressing key: {str(e)}. Valid keys: enter, tab, escape, space, command, etc."
        )


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
        with open(os.path.expanduser(filepath)) as f:
            lines = f.readlines()[:max_lines]
            content = "".join(lines)
            truncated = " (truncated)" if len(f.readlines()) > max_lines else ""
            return f"📄 Content of {filepath}{truncated}:\n{content}"
    except FileNotFoundError:
        return f"❌ File not found: {filepath}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


@tool
def list_directory(directory_path: str):
    """Lists all files and folders in a directory with details (size, type, name).
    ALWAYS use this FIRST when organizing files - you need to see what actually exists!
    Don't assume what files are there - LOOK first, then decide what to do.
    Example: list_directory('~/Desktop')"""
    if not is_safe(directory_path):
        return "🚫 Unsafe path blocked."
    try:
        path = os.path.expanduser(directory_path)
        if not os.path.exists(path):
            return f"❌ Directory not found: {directory_path}"

        items = []
        file_types = {}  # Track what file types exist

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                ext = os.path.splitext(item)[1].lower()
                items.append(f"📄 {item} ({ext}, {size} bytes)")
                # Track file extensions
                if ext:
                    file_types[ext] = file_types.get(ext, 0) + 1
            elif os.path.isdir(item_path):
                items.append(f"📁 {item}/")

        if not items:
            return f"📂 Directory {directory_path} is empty"

        result = f"📂 Contents of {directory_path}:\n" + "\n".join(items)

        # Add intelligence: show summary of file types
        if file_types:
            result += "\n\n📊 File types found: "
            result += ", ".join([f"{count} {ext}" for ext, count in sorted(file_types.items())])

        return result
    except PermissionError:
        return f"❌ Permission denied: {directory_path}"
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"


@tool
def plan_task(task_description: str, observations: str = ""):
    """Create a smart plan BEFORE taking action. Use this to think through your approach.

    This tool helps you:
    - Break down the task into logical steps
    - Identify what information you need
    - Decide which tools to use and in what order
    - Avoid unnecessary actions

    Args:
        task_description: What the user asked you to do
        observations: What you've learned so far (e.g., "Desktop has 3 JPGs, 2 PDFs")

    Returns: A structured plan with reasoning

    Example:
        plan_task(
            "Organize Desktop by file type",
            "Desktop has: 3 .jpg files, 2 .pdf files, 1 .mp4 file"
        )
    """
    plan = f"""
🎯 TASK PLANNING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 User Request: {task_description}

🔍 Current Observations:
{observations if observations else "   (No observations yet - need to gather info first)"}

💡 INTELLIGENT ANALYSIS:
"""

    if observations:
        # Parse what file types exist
        plan += "\n   Based on what I see, I should:\n"
        plan += "   1. Only create folders for file types that ACTUALLY exist\n"
        plan += "   2. Don't create empty folders that won't be used\n"
        plan += "   3. Group similar file types logically\n"
        plan += "\n   Recommended actions:\n"

        # Suggest folder categories based on common patterns
        if any(ext in observations.lower() for ext in [".jpg", ".jpeg", ".png", ".gif"]):
            plan += "   → Create 'Images' folder (for image files)\n"
        if any(ext in observations.lower() for ext in [".pdf", ".doc", ".txt"]):
            plan += "   → Create 'Documents' folder (for document files)\n"
        if any(ext in observations.lower() for ext in [".mp4", ".mov", ".avi"]):
            plan += "   → Create 'Videos' folder (for video files)\n"
        if any(ext in observations.lower() for ext in [".mp3", ".wav", ".flac"]):
            plan += "   → Create 'Audio' folder (for audio files)\n"
        if any(ext in observations.lower() for ext in [".zip", ".rar", ".7z"]):
            plan += "   → Create 'Archives' folder (for compressed files)\n"

        plan += "\n   ⚠️  DON'T create folders for file types that don't exist!\n"
    else:
        plan += "\n   Step 1: GATHER INFORMATION\n"
        plan += "   → Use list_directory() to see what files exist\n"
        plan += "   → Analyze the file types present\n"
        plan += "\n   Step 2: CREATE SMART PLAN\n"
        plan += "   → Call plan_task() again with observations\n"
        plan += "   → Decide which folders are actually needed\n"

    plan += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Remember: Adapt to the actual situation. Think, don't template-follow!
"""

    return plan


@tool
def self_critique(original_task: str, actions_summary: str, expected_outcome: str):
    """CRITICAL: Evaluate if you actually completed the task BEFORE saying done.

    Use this to check yourself:
    - Did I fully complete what user asked?
    - Did I just do part of it?
    - What's missing?
    - Should I continue working?

    Args:
        original_task: What the user originally asked for
        actions_summary: What actions you took (be honest!)
        expected_outcome: What should have happened

    Returns: Self-assessment with completion percentage and missing items

    Example:
        Task: "Organize Desktop by moving images to Images folder"
        Actions: "Created Images folder"
        Expected: "All image files moved to Images folder"

        Result: "⚠️ Only 20% complete - Created folder but didn't move any files!"
    """
    # This is a meta-tool - helps AI evaluate itself
    critique = f"""
🔍 SELF-CRITIQUE ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Original Task:
   {original_task}

✅ Actions I Actually Took:
   {actions_summary}

🎯 What Should Have Happened:
   {expected_outcome}

⚠️ HONEST ASSESSMENT:
"""

    # Simple completion check
    action_words = actions_summary.lower().split()
    expected_words = expected_outcome.lower().split()

    # Check for key action verbs
    critical_actions = ["moved", "copied", "deleted", "created", "modified", "organized"]
    actions_done = sum(1 for action in critical_actions if action in action_words)
    actions_needed = sum(1 for action in critical_actions if action in expected_words)

    completion = actions_done / actions_needed * 100 if actions_needed > 0 else 50  # Unknown

    if completion < 50:
        critique += f"   🔴 INCOMPLETE ({completion:.0f}%)\n"
        critique += "   ❌ Major gaps detected - continue working!\n"
    elif completion < 90:
        critique += f"   🟡 PARTIAL ({completion:.0f}%)\n"
        critique += "   ⚠️  Some steps missing - verify and complete!\n"
    else:
        critique += f"   🟢 COMPLETE ({completion:.0f}%)\n"
        critique += "   ✅ Task appears fully done!\n"

    critique += "\n💡 RECOMMENDATION:\n"
    if completion < 90:
        critique += "   → DO NOT say 'Done' yet\n"
        critique += "   → Identify what's missing\n"
        critique += "   → Complete remaining steps\n"
        critique += "   → Then run self_critique again\n"
    else:
        critique += "   → Verify results one more time\n"
        critique += "   → Then you can report completion\n"

    return critique


@tool
def verify_expectations(what_to_verify: str, verification_commands: str):
    """Verify that expected changes actually happened.

    Use this to confirm your actions worked as intended.

    Args:
        what_to_verify: What you expect to find (e.g., "8 JPG files in ~/Desktop/Images/")
        verification_commands: Shell commands to check (e.g., "ls ~/Desktop/Images/*.jpg | wc -l")

    Returns: Verification result - did expectations match reality?

    Example:
        verify_expectations(
            "All JPG files should be in Images folder",
            "ls ~/Desktop/Images/*.jpg"
        )
    """
    if not is_safe(verification_commands):
        return "🚫 Unsafe verification command blocked."

    try:
        result = subprocess.run(
            verification_commands, shell=True, capture_output=True, text=True, timeout=10
        )

        output = result.stdout if result.stdout else result.stderr

        verification_result = f"""
🔍 VERIFICATION REPORT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Expected:
   {what_to_verify}

🔧 Verification Command:
   {verification_commands}

📊 Actual Result:
{output}

"""

        if result.returncode == 0 and output.strip():
            verification_result += "✅ VERIFICATION PASSED\n   Expected conditions met!"
        elif result.returncode == 0 and not output.strip():
            verification_result += "⚠️  VERIFICATION INCONCLUSIVE\n   No output - might be empty"
        else:
            verification_result += "❌ VERIFICATION FAILED\n   Expected conditions NOT met!"

        return verification_result

    except Exception as e:
        return f"❌ Verification error: {str(e)}"


# ============================================================================
# PERSISTENT MEMORY SYSTEM - Remembers across sessions
# ============================================================================

MEMORY_FILE = os.path.expanduser("~/.ai_robot_memory.json")


def _load_memory():
    """Internal: Load memory from file"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"preferences": {}, "facts": {}, "mistakes": [], "successes": []}
    return {"preferences": {}, "facts": {}, "mistakes": [], "successes": []}


def _save_memory(memory_data):
    """Internal: Save memory to file"""
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=2)
        return True
    except Exception:
        return False


@tool
def save_to_memory(key: str, value: str, memory_type: str = "fact"):
    """Save information to PERMANENT memory (persists across sessions).

    Use this to remember:
    - User preferences ("user likes absolute paths")
    - Important facts ("Desktop path is ~/Desktop")
    - Mistakes to avoid ("mkdir without checking existence fails")
    - Successful strategies ("use 'mv *.jpg' for bulk moves")

    Args:
        key: Short identifier (e.g., "user_path_preference")
        value: What to remember (e.g., "User prefers absolute paths like ~/Desktop")
        memory_type: Type of memory - "preference", "fact", "mistake", "success"

    Returns: Confirmation of what was saved

    Example:
        save_to_memory(
            "organize_files_pattern",
            "Always list directory first, then create folders, then move files",
            "success"
        )
    """
    memory = _load_memory()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"value": value, "timestamp": timestamp}

    if memory_type == "preference":
        memory["preferences"][key] = entry
    elif memory_type == "fact":
        memory["facts"][key] = entry
    elif memory_type == "mistake":
        memory["mistakes"].append({"key": key, **entry})
    elif memory_type == "success":
        memory["successes"].append({"key": key, **entry})
    else:
        return f"❌ Invalid memory type: {memory_type}. Use: preference, fact, mistake, or success"

    if _save_memory(memory):
        return f"💾 Saved to memory [{memory_type}]: {key} = {value}"
    else:
        return "❌ Failed to save memory"


@tool
def recall_from_memory(query: str = "all"):
    """Recall information from PERMANENT memory.

    Use this to:
    - Check user preferences before acting
    - Avoid repeating past mistakes
    - Use successful strategies from before
    - Remember important facts

    Args:
        query: What to recall - "all", "preferences", "facts", "mistakes", "successes", or a keyword

    Returns: Relevant memories

    Example:
        recall_from_memory("path")  # Finds all memories about paths
        recall_from_memory("preferences")  # Shows all user preferences
    """
    memory = _load_memory()

    if query == "all":
        total = (
            len(memory["preferences"])
            + len(memory["facts"])
            + len(memory["mistakes"])
            + len(memory["successes"])
        )
        result = f"📚 MEMORY BANK ({total} total memories)\n\n"

        if memory["preferences"]:
            result += "👤 USER PREFERENCES:\n"
            for key, data in memory["preferences"].items():
                result += f"   • {key}: {data['value']}\n"

        if memory["facts"]:
            result += "\n📋 FACTS:\n"
            for key, data in memory["facts"].items():
                result += f"   • {key}: {data['value']}\n"

        if memory["mistakes"]:
            result += "\n⚠️  MISTAKES TO AVOID (last 5):\n"
            for item in memory["mistakes"][-5:]:
                result += f"   • {item['key']}: {item['value']}\n"

        if memory["successes"]:
            result += "\n✅ SUCCESSFUL STRATEGIES (last 5):\n"
            for item in memory["successes"][-5:]:
                result += f"   • {item['key']}: {item['value']}\n"

        return result if total > 0 else "📚 Memory is empty - nothing learned yet!"

    elif query in ["preferences", "facts", "mistakes", "successes"]:
        items = memory.get(query, {})
        if isinstance(items, dict):
            return f"{query.upper()}:\n" + "\n".join(
                [f"• {k}: {v['value']}" for k, v in items.items()]
            )
        else:
            return f"{query.upper()}:\n" + "\n".join(
                [f"• {item['key']}: {item['value']}" for item in items[-10:]]
            )

    else:
        # Search for keyword
        results = []
        query_lower = query.lower()

        for key, data in memory["preferences"].items():
            if query_lower in key.lower() or query_lower in data["value"].lower():
                results.append(f"[PREFERENCE] {key}: {data['value']}")

        for key, data in memory["facts"].items():
            if query_lower in key.lower() or query_lower in data["value"].lower():
                results.append(f"[FACT] {key}: {data['value']}")

        for item in memory["mistakes"]:
            if query_lower in item["key"].lower() or query_lower in item["value"].lower():
                results.append(f"[MISTAKE] {item['key']}: {item['value']}")

        for item in memory["successes"]:
            if query_lower in item["key"].lower() or query_lower in item["value"].lower():
                results.append(f"[SUCCESS] {item['key']}: {item['value']}")

        if results:
            return f"🔍 Found {len(results)} memories about '{query}':\n\n" + "\n\n".join(results)
        else:
            return f"❌ No memories found for '{query}'"


@tool
def clear_memory(memory_type: str = "all"):
    """Clear memory (use carefully!).

    Args:
        memory_type: What to clear - "all", "preferences", "facts", "mistakes", or "successes"

    Returns: Confirmation
    """
    memory = _load_memory()

    if memory_type == "all":
        memory = {"preferences": {}, "facts": {}, "mistakes": [], "successes": []}
        message = "🗑️  Cleared ALL memory"
    elif memory_type in memory:
        if isinstance(memory[memory_type], dict):
            memory[memory_type] = {}
        else:
            memory[memory_type] = []
        message = f"🗑️  Cleared {memory_type}"
    else:
        return f"❌ Invalid memory type: {memory_type}"

    _save_memory(memory)
    return message


# ============================================================================
# ROBUST ERROR RECOVERY SYSTEM
# ============================================================================


@tool
def debug_last_error(error_message: str, command_that_failed: str, context: str = ""):
    """When something fails, use this to get debugging help and alternative strategies.

    This tool analyzes errors and suggests 5+ alternative approaches to try.

    Args:
        error_message: The error you got (e.g., "Permission denied")
        command_that_failed: What you tried (e.g., "mkdir ~/Desktop/Images")
        context: What you were trying to accomplish (e.g., "organizing files")

    Returns: Error analysis + multiple alternative strategies ranked by success probability

    Example:
        debug_last_error(
            "Permission denied",
            "mv files to /System/",
            "trying to organize system files"
        )
    """

    analysis = f"""
🐛 ERROR DEBUGGING REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ ERROR: {error_message}
🔧 FAILED COMMAND: {command_that_failed}
📋 CONTEXT: {context or "No context provided"}

🔍 ERROR ANALYSIS:
"""

    # Categorize error and provide solutions
    error_lower = error_message.lower()

    if "permission denied" in error_lower or "operation not permitted" in error_lower:
        analysis += """
   Type: PERMISSION ERROR

   Why it failed:
   • File/directory is protected
   • Current user doesn't have write access
   • System location requires elevated permissions

   🔄 ALTERNATIVE STRATEGIES (try in order):

   1. ⭐⭐⭐⭐⭐ Use a different location
      → Try ~/Desktop or ~/Documents instead of system folders
      → Command: mkdir ~/Desktop/FolderName

   2. ⭐⭐⭐⭐ Check and change permissions
      → See current permissions: ls -la <path>
      → Change if safe: chmod u+w <path>

   3. ⭐⭐⭐ Use absolute paths
      → Instead of relative paths, use full ~/path/to/file
      → This avoids permission issues in current directory

   4. ⭐⭐ Check file ownership
      → See owner: ls -l <path>
      → Make sure it's your file

   5. ⭐ Create in user space first
      → Create in ~/ first, then copy to destination
"""

    elif "command not found" in error_lower or "no such file or directory" in error_lower:
        analysis += """
   Type: COMMAND/FILE NOT FOUND

   Why it failed:
   • Command doesn't exist
   • File path is wrong
   • Tool not installed

   🔄 ALTERNATIVE STRATEGIES (try in order):

   1. ⭐⭐⭐⭐⭐ Try alternative command
      → wget → curl
      → apt-get → brew (on Mac)
      → python → python3

   2. ⭐⭐⭐⭐ Check if path exists first
      → Use: list_directory() to see what's actually there
      → Verify paths before using them

   3. ⭐⭐⭐ Use absolute paths
      → Instead of "file.txt" → use "~/Desktop/file.txt"
      → Less ambiguity

   4. ⭐⭐ Install missing tool
      → Mac: brew install <tool>
      → Check: which <command>

   5. ⭐ Search for the file
      → Use: search_file() tool
      → Find where it actually is
"""

    elif "already exists" in error_lower or "file exists" in error_lower:
        analysis += """
   Type: FILE/FOLDER ALREADY EXISTS

   Why it failed:
   • Target already exists
   • Trying to overwrite

   🔄 ALTERNATIVE STRATEGIES (try in order):

   1. ⭐⭐⭐⭐⭐ Check existence FIRST
      → Use: list_directory() before creating
      → Avoid collision

   2. ⭐⭐⭐⭐ Use a different name
      → Add timestamp: Images_2024_01_15
      → Add number: Images_2

   3. ⭐⭐⭐ Remove old one first
      → Check: ls <path>
      → Delete: rm <path> (if safe!)
      → Then create new

   4. ⭐⭐ Use force flag carefully
      → Add -f flag to overwrite
      → BE CAREFUL - this deletes existing!

   5. ⭐ Merge instead of replace
      → Move contents into existing folder
      → Don't create new one
"""

    elif "is a directory" in error_lower or "is not a directory" in error_lower:
        analysis += """
   Type: DIRECTORY/FILE MISMATCH

   Why it failed:
   • Treating file as directory or vice versa

   🔄 ALTERNATIVE STRATEGIES (try in order):

   1. ⭐⭐⭐⭐⭐ Check what it actually is
      → Use: list_directory() on parent
      → See if it's file or folder

   2. ⭐⭐⭐⭐ Use correct command
      → For files: cat, mv, cp
      → For directories: cd, mkdir, rmdir

   3. ⭐⭐⭐ Check path carefully
      → Make sure path is correct
      → No typos in folder names
"""

    elif "no space" in error_lower or "disk full" in error_lower:
        analysis += """
   Type: DISK SPACE ERROR

   Why it failed:
   • Not enough disk space

   🔄 ALTERNATIVE STRATEGIES:

   1. ⭐⭐⭐⭐⭐ Check disk space
      → Command: df -h
      → See what's available

   2. ⭐⭐⭐⭐ Clean up first
      → Remove temporary files
      → Empty trash

   3. ⭐⭐⭐ Use different location
      → Try external drive
      → Use cloud storage
"""

    else:
        # Generic error
        analysis += """
   Type: GENERAL ERROR

   🔄 GENERIC TROUBLESHOOTING STRATEGIES:

   1. ⭐⭐⭐⭐⭐ Read error message carefully
      → Look for specific hints
      → Error messages usually tell you what's wrong

   2. ⭐⭐⭐⭐ Verify inputs
      → Check paths exist: list_directory()
      → Verify parameters are correct

   3. ⭐⭐⭐ Try simpler version
      → Break command into smaller steps
      → Test each part separately

   4. ⭐⭐ Check context
      → Am I in the right directory? get_current_directory()
      → Do I have the right permissions?

   5. ⭐ Try completely different approach
      → If file operations fail, try GUI automation
      → If command-line fails, try Python code
"""

    analysis += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 NEXT STEPS:
1. Pick highest-rated strategy (⭐⭐⭐⭐⭐)
2. Try it
3. If fails, try next strategy
4. DON'T GIVE UP - work through all alternatives!
5. Save what worked: save_to_memory(strategy, "success")
"""

    return analysis
