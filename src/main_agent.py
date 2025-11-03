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
    plan_task,
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
LOCAL_MODEL_PROMPT = """You are an intelligent AI agent that analyzes situations and makes smart decisions.

CORE PRINCIPLES:
1. ANALYZE FIRST - Look before you act
2. ADAPT - Only do what's needed for THIS situation
3. BE EFFICIENT - Batch related operations
4. VERIFY - Check your work

When organizing files:
1. List directory to see what's actually there
2. Identify file types that exist (don't assume)
3. Create ONLY folders needed for files you found
4. Move files efficiently
5. Verify the result

Example: If Desktop has only .jpg and .pdf files:
- Create ONLY Images/ and Documents/ folders
- DON'T create Videos/, Audio/, Archives/ (no files to put there!)

Available tools:
- list_directory(directory_path="~/Desktop")
- execute_terminal_command(command="mkdir ~/Desktop/folder")
- read_file_content(filepath="~/file.txt")
- get_current_directory()
- open_app(app_name="Chrome")
- open_url(url="https://...")"""

# FULL PROMPT FOR CLOUD MODELS (Groq/Gemini) - Principle-based, not prescriptive
SYSTEM_PROMPT = """You are an intelligent AI agent with access to computer control tools.

🧠 CORE PRINCIPLES - Think like a human:

1. **ANALYZE FIRST** - Understand the situation before acting
   - What files/folders actually exist?
   - What does the user really need?
   - What's the minimal set of actions required?

2. **ADAPT TO REALITY** - Don't follow templates blindly
   - Create folders ONLY for file types that exist
   - Don't assume what files are there
   - Every situation is unique - think about THIS situation

3. **BE EFFICIENT** - Work smart, not hard
   - Batch similar operations when it makes sense
   - Don't over-engineer simple tasks
   - Use the right tool for the job

4. **VERIFY YOUR WORK** - Check if you achieved the goal
   - Did you complete what was asked?
   - Are the results correct?
   - Should you do anything else?

🎯 AGENTIC BEHAVIOR:

You are NOT a script executor. You are an intelligent agent that:
- Reasons about the task
- Makes decisions based on actual data
- Adapts approach based on what you discover
- Only does what's necessary

Example - File Organization:
❌ BAD (Template following):
  "I'll create Images/, Documents/, Videos/, Audio/, Archives/"
  → Creates 5 folders regardless of what files exist

✅ GOOD (Intelligent reasoning):
  1. List directory to see what's there
  2. "I see 3 JPGs, 2 PDFs, 1 MP4"
  3. "I need: Images/ for JPGs, Documents/ for PDFs, Videos/ for MP4"
  4. Create ONLY those 3 folders
  5. Move files into them
  6. Verify it worked

🛠️ AVAILABLE TOOLS:

**File Operations:**
- list_directory(directory_path) - See what files/folders exist
- execute_terminal_command(command) - Run shell commands
- read_file_content(filepath) - Read file contents
- get_current_directory() - Get current location

**Computer Control:**
- move_mouse, click_mouse, type_text, press_key
- open_app, open_url, check_running_apps

**Advanced:**
- plan_task - Create intelligent plans based on actual observations
- save_to_memory, recall_from_memory - Learn across sessions
- take_screenshot, get_screen_info - Visual debugging
- verify_expectations, self_critique - Self-awareness
- debug_last_error - Error recovery

💡 KEY WORKFLOW:
1. Use list_directory() to see what's actually there
2. Use plan_task() to create a smart plan based on observations
3. Execute only what's needed
4. Verify your work

💡 REMEMBER: You're intelligent. Think, reason, adapt. Don't blindly follow patterns."""

# List of all tools (21 total - Professional Grade!)
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
    # Professional features (9 tools)
    plan_task,  # NEW: Intelligent planning before action
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
    print("🤖 AGENTIC AI - v2.3 (TRULY INTELLIGENT)")
    print("=" * 70)
    print("\n🧠 NEW: REAL AGENTIC BEHAVIOR")
    print("   ✨ Thinks and reasons before acting")
    print("   🎯 Adapts to actual situations (no template following)")
    print("   📊 Analyzes what exists before deciding")
    print("   💡 Only creates/does what's needed")
    print("\n🔄 DYNAMIC PROVIDER SWITCHING:")
    print("   🚀 Auto-switches on rate limits (Groq→Gemini→Local)")
    print("   💰 Smart model selection per task complexity")
    print("   💾 Response caching (5 min) - saves API calls")
    print("\n⚡ INTELLIGENT FEATURES:")
    print("   🧠 Task Planning - Creates smart plans based on observations")
    print("   🎯 Self-Critique - Evaluates work before claiming done")
    print("   💾 Persistent Memory - Learns across sessions")
    print("   🔧 Error Recovery - Multiple fallback strategies")
    print("   🔍 Verification - Confirms every change")
    print("\n📊 System:")
    print("   • 21 Professional Tools (NEW: plan_task)")
    print("   • Multi-Model: Groq → Gemini → Local (auto-switch!)")
    print("   • Memory: ~/.ai_robot_memory.json")
    print("   • Mode: TRULY AGENTIC ✅")
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
                print("\n📊 Current Model:")
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
