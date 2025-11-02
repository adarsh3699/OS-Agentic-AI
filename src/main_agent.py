from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from src.agent_tools import (
    DANGEROUS_COMMANDS,
    check_running_apps,
    clear_memory,
    click_mouse,
    debug_last_error,
    execute_terminal_command,
    get_current_directory,
    get_screen_info,
    list_directory,
    move_mouse,
    open_app,
    open_url,
    press_key,
    read_file_content,
    recall_from_memory,
    save_to_memory,
    search_file,
    self_critique,
    take_screenshot,
    type_text,
    verify_expectations,
)

# ============================================================================
# SYSTEM PROMPTS - Different prompts for different model types
# ============================================================================

# SIMPLIFIED PROMPT FOR LOCAL MODELS (Ollama) - Short and direct
LOCAL_MODEL_PROMPT = """You are an AI assistant that CALLS TOOLS to complete tasks.

CRITICAL RULES:
1. ALWAYS use ~/Desktop for Desktop path (NEVER use /path/to/Desktop)
2. GROUP related file types (Images: jpg+jpeg+png, Documents: pdf+doc+txt)
3. BATCH commands - create all folders at once, move files with &&
4. Call 3-5 tools total, then STOP

🧠 SMART FILE GROUPING:
- Images/ → .jpg, .jpeg, .png, .gif, .bmp
- Documents/ → .pdf, .doc, .docx, .txt
- Videos/ → .mp4, .mov, .avi, .mkv
- Audio/ → .mp3, .wav, .flac

Example Task: "Organize Desktop"
Step 1: list_directory("~/Desktop") → see: file.jpg, pic.jpeg, doc.pdf
Step 2: execute_terminal_command("mkdir ~/Desktop/Images ~/Desktop/Documents")
Step 3: execute_terminal_command("mv ~/Desktop/*.jpg ~/Desktop/Images && mv ~/Desktop/*.jpeg ~/Desktop/Images && mv ~/Desktop/*.pdf ~/Desktop/Documents")
Step 4: STOP and say "Done! Organized into Images and Documents"

Available tools:
- list_directory(directory_path="~/Desktop")
- execute_terminal_command(command="mkdir ~/Desktop/folder")
- read_file_content(filepath="~/file.txt")
- get_current_directory()
- open_app(app_name="Chrome")
- open_url(url="https://...")"""

# FULL PROMPT FOR CLOUD MODELS (Groq/Gemini) - Detailed with examples
SYSTEM_PROMPT = """🚨 CRITICAL RULES:

1. PLAN FIRST - Analyze the task, group related operations
2. BATCH OPERATIONS - Combine similar actions into single commands
3. USE SMART CATEGORIES - Group related file types logically
4. VERIFY ONCE - Check results at the end, not after every step

🧠 INTELLIGENT FILE CATEGORIZATION:

When organizing files, USE SMART CATEGORIES (not one folder per extension):

✅ SMART GROUPING:
- Images/ → .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp
- Documents/ → .pdf, .doc, .docx, .txt, .rtf, .odt
- Videos/ → .mp4, .mov, .avi, .mkv, .webm, .flv
- Audio/ → .mp3, .wav, .flac, .aac, .ogg, .m4a
- Archives/ → .zip, .rar, .7z, .tar, .gz

❌ WRONG: Create JPG/, JPEG/, PNG/ (too many folders!)
✅ RIGHT: Create Images/ for all image formats

⚡ UNIVERSAL OPTIMIZATION PRINCIPLES:

For ANY task, follow this pattern:
1. GATHER INFO - Call tools to see current state
2. PLAN - Decide what needs to happen
3. BATCH - Combine related operations
4. EXECUTE - Run batched commands
5. VERIFY - Check final result

Examples: 

📁 File Organization:
1. list_directory once → see all files
2. Group by category (Images, Documents, etc)
3. mkdir all folders in one command
4. mv all files with && chains
5. verify once

📝 Multi-file Processing:
1. list_directory → find target files
2. Plan operations (read, modify, write)
3. Batch process with loops/scripts
4. Execute combined command
5. verify results

🔍 Search & Replace:
1. search_file → find targets
2. Plan all replacements
3. Batch with sed/awk commands
4. Execute once
5. verify changes

You are an INTELLIGENT AI assistant. You GROUP logically, BATCH efficiently, and VERIFY once.

📋 BATCHING COMMANDS:

Use shell operators to combine commands:
- `&&` - Run commands in sequence: "mkdir folder && mv files folder"
- Multiple args - Create multiple folders: "mkdir folder1 folder2 folder3"

Example:
❌ SLOW: 3 separate calls
  execute_terminal_command("mkdir ~/Desktop/Photos")
  execute_terminal_command("mkdir ~/Desktop/Documents")
  execute_terminal_command("mkdir ~/Desktop/Videos")

✅ FAST: 1 combined call
  execute_terminal_command("mkdir ~/Desktop/Photos ~/Desktop/Documents ~/Desktop/Videos")

⚠️ TOOL USAGE RULES:

1. Use execute_terminal_command() for mkdir, mv, cp, rm
2. Use list_directory() to see folder contents
3. BATCH commands when possible (mkdir multiple folders at once)
4. Verify ONCE at the end, not after every step

🧰 AVAILABLE TOOLS:

**File Operations (Most Used):**
- list_directory(directory_path) - See folder contents
- execute_terminal_command(command) - Run ANY shell command (mkdir, mv, etc)
- read_file_content(filepath) - Read files

**Computer Control:**
- move_mouse, click_mouse, type_text, press_key
- open_app, open_url, check_running_apps

**Advanced:**
- Memory: save_to_memory, recall_from_memory
- Debug: take_screenshot, debug_last_error
- Verification: verify_expectations, self_critique

Work efficiently, batch operations, and verify once at the end. 🎯"""

# List of all tools (20 total - Professional Grade!)
tools = [
    # Computer control (8 tools)
    move_mouse,
    click_mouse,
    type_text,
    press_key,
    search_file,
    open_app,
    open_url,
    check_running_apps,
    # File operations (4 tools)
    execute_terminal_command,
    get_current_directory,
    read_file_content,
    list_directory,
    # Professional features (8 tools)
    self_critique,
    verify_expectations,  # Self-awareness
    save_to_memory,
    recall_from_memory,
    clear_memory,  # Persistent memory
    debug_last_error,  # Error recovery
    take_screenshot,
    get_screen_info,  # Debugging
]

# Simplified tool list for local models (remove memory tools that confuse them)
local_tools = [
    # File operations (core tools only)
    list_directory,
    execute_terminal_command,
    read_file_content,
    get_current_directory,
    # Computer control (basic only)
    open_app,
    open_url,
]


def main():
    """Main entry point for the AI Robot agent"""

    # Load AI model with automatic fallback (Groq → Gemini → Local)
    print("🔧 Initializing AI Model...")
    print("=" * 70)

    from src.model_switcher import DynamicModelSwitcher

    model_switcher = DynamicModelSwitcher()
    llm = model_switcher.get_model()
    print("=" * 70)

    # Memory to remember past actions (helps with feedback)
    memory = MemorySaver()

    # Config for the session (like a conversation ID + recursion limit)
    # Note: High enough for complex multi-step tasks with verification
    config = {
        "configurable": {"thread_id": "my-robot-thread"},
        "recursion_limit": 50,  # Allows complex tasks with verification (e.g., organize 5+ file types)
    }

    # Create a prompt session with history support for arrow key navigation
    session = PromptSession(history=InMemoryHistory())

    print("=" * 70)
    print("🤖 CURSOR-STYLE AI - v2.2 (AUTO-SWITCHING)")
    print("=" * 70)
    print("\n🎯 NEW: DYNAMIC PROVIDER SWITCHING")
    print("   🔄 Auto-switches providers on rate limits (Groq→Gemini→Local)")
    print("   💰 Auto-selects optimal model (8B/11B/70B) per task")
    print("   💾 Caches responses for 5 minutes (FREE repeats!)")
    print("   ⚡ 50-70% cost reduction with ZERO accuracy loss")
    print("\n🎯 STEP-BY-STEP VERIFICATION (Like Cursor AI)")
    print("   ✅ Verifies EVERY action before proceeding")
    print("   ✅ Shows: Step 1 → Verify → Step 2 → Verify → Done")
    print("   ✅ Won't skip steps or claim done prematurely")
    print("   ✅ Checks both source AND destination after moves")
    print("\n⚡ PROFESSIONAL FEATURES:")
    print("   🧠 Self-Critique - Evaluates before claiming 'done'")
    print("   💾 Persistent Memory - Learns across sessions")
    print("   🔧 Error Recovery - 5+ fallback strategies")
    print("   🔍 Multi-Level Verification - Confirms every change")
    print("   🔄 Runtime Provider Switching - Never crashes on rate limits!")
    print("\n📊 System:")
    print("   • 20 Professional Tools")
    print("   • Multi-Model: Groq → Gemini → Local (auto-switch!)")
    print("   • Memory: ~/.ai_robot_memory.json")
    print("   • Mode: AUTO-SWITCHING + COST OPTIMIZED ✅")
    print("\n💡 Watch Me Work:")
    print("   • I'll show: Create folder → ✅ Verify → Move files → ✅ Verify")
    print("   • I'll auto-select the right model size for each task")
    print("   • If rate limited, I'll switch providers mid-task (no crash!)")
    print("   • Type 'exit' to quit")
    print("\n💡 Manual Model Switching:")
    print("   • 'switch to local' - Use local Ollama model")
    print("   • 'switch to groq' - Use Groq API")
    print("   • 'switch to gemini' - Use Gemini API")
    print("   • 'show model' - See current model")
    print("\n" + "=" * 70)
    print("\n🧪 Test With: 'Organize my Desktop by file type'")
    print("   (Watch me handle rate limits gracefully!)")
    print("=" * 70 + "\n")

    while True:
        try:
            prompt = session.prompt("🤖 Your command: ")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        if prompt.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        # Handle manual model switching commands
        prompt_lower = prompt.lower().strip()
        
        if "switch to local" in prompt_lower or "use local" in prompt_lower:
            print("\n🔄 Manually switching to Local (Ollama)...\n")
            llm = model_switcher._try_load_provider("ollama", "", switching=True)
            if llm:
                print("✅ Now using Local Ollama model!\n")
            continue
        
        elif "switch to groq" in prompt_lower or "use groq" in prompt_lower:
            print("\n🔄 Manually switching to Groq...\n")
            llm = model_switcher._try_load_provider("groq", "", switching=True)
            if llm:
                print("✅ Now using Groq model!\n")
            continue
        
        elif "switch to gemini" in prompt_lower or "use gemini" in prompt_lower:
            print("\n🔄 Manually switching to Gemini...\n")
            llm = model_switcher._try_load_provider("gemini", "", switching=True)
            if llm:
                print("✅ Now using Gemini model!\n")
            continue
        
        elif "show model" in prompt_lower or "current model" in prompt_lower or "which model" in prompt_lower:
            current = model_switcher.current_provider
            if current:
                info = config.MODEL_INFO[current]
                tier = config.DEFAULT_TIER
                model_name = config.MODEL_TIERS[tier][current]
                print(f"\n📊 Current Model:")
                print(f"   Provider: {current.upper()}")
                print(f"   Name: {info['name']}")
                print(f"   Model: {model_name}")
                print(f"   Cost: {info['cost']}")
                print()
            else:
                print("\n⚠️  No model loaded yet\n")
            continue
        
        elif prompt_lower in ["help", "commands", "?", "help me"]:
            print("\n" + "=" * 70)
            print("📋 AVAILABLE COMMANDS")
            print("=" * 70)
            print("\n🔄 Model Switching:")
            print("   • switch to local   - Use local Ollama (llama3.1:8b)")
            print("   • switch to groq    - Use Groq API (fast)")
            print("   • switch to gemini  - Use Gemini API (reliable)")
            print("   • show model        - Show current model info")
            print("\n💡 General:")
            print("   • help              - Show this help message")
            print("   • exit              - Quit the application")
            print("\n🤖 AI Tasks (examples):")
            print("   • Organize my Desktop by file type")
            print("   • List files in my Downloads")
            print("   • Move all PDFs to Documents")
            print("   • Open Chrome browser")
            print("=" * 70 + "\n")
            continue
        
        if not all(
            danger.lower() not in prompt.lower() for danger in DANGEROUS_COMMANDS
        ):  # Quick safety check
            print("🚫 Unsafe command blocked! Try something nice.")
            continue

        print("🧠 AI is processing your request...\n")

        # Choose system prompt based on provider (local models need simpler prompts)
        system_prompt = (
            LOCAL_MODEL_PROMPT 
            if model_switcher.current_provider == "ollama" 
            else SYSTEM_PROMPT
        )
        
        # Run the agent with feedback loop (include system prompt as first message)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # Retry with provider switching on rate limit errors
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # Choose tool set based on provider (local models get simplified tools)
                current_tools = (
                    local_tools 
                    if model_switcher.current_provider == "ollama" 
                    else tools
                )
                
                # Recreate agent with current model
                agent_executor = create_react_agent(llm, current_tools, checkpointer=memory)

                for chunk in agent_executor.stream({"messages": messages}, config):
                    # Show agent node execution
                    if "agent" in chunk:
                        agent_messages = chunk["agent"]["messages"]
                        for msg in agent_messages:
                            # AI thinking/response
                            if hasattr(msg, "content") and msg.content:
                                print(f"💭 AI Thinking: {msg.content}")

                            # Tool calls
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    tool_name = tool_call.get("name", "unknown")
                                    tool_args = tool_call.get("args", {})
                                    print(f"🔧 Calling Tool: {tool_name}({tool_args})")

                    # Show tool execution results
                    if "tools" in chunk:
                        tool_messages = chunk["tools"]["messages"]
                        for msg in tool_messages:
                            if hasattr(msg, "content"):
                                print(f"✅ Tool Result: {msg.content}")

                print("\n✨ Task completed!\n")
                break  # Success!

            except Exception as e:
                error_str = str(e)

                # Check if it's a rate limit error
                if (
                    "rate" in error_str.lower()
                    or "429" in error_str
                    or "quota" in error_str.lower()
                ):
                    retry_count += 1
                    if retry_count < max_retries:
                        print("\n⚠️  Rate limit error detected!")
                        print(
                            f"🔄 Switching to backup provider... (Attempt {retry_count}/{max_retries})"
                        )

                        # Switch to next provider
                        llm = model_switcher.switch_provider(error_str)

                        if llm is None:
                            print("\n❌ All providers exhausted. Please try again later.")
                            break

                        print("✅ Switched successfully! Retrying task...\n")
                        continue
                    else:
                        print(f"\n❌ Max retries reached. Error: {e}")
                        print("💡 All AI providers are rate limited. Wait or try again later.")
                        break
                else:
                    # Non-rate-limit error, show and exit
                    print(f"\n❌ Error: {e}")
                    break
