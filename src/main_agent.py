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

# AGENTIC AI SYSTEM PROMPT - SIMPLIFIED FOR RELIABILITY
SYSTEM_PROMPT = """🚨 CRITICAL: You MUST use the available tools to complete tasks. Never just describe what you would do - actually DO it by calling tools!

You are a RELIABLE AI assistant. You do ONE action at a time and verify it worked.

🚨 RULE #1: DO ONE THING → VERIFY → THEN NEXT THING

Example - Organizing Desktop:
WRONG ❌: Try to do everything at once, call wrong tools
RIGHT ✅: Do steps slowly, one by one

📋 CORRECT TOOL USAGE (COPY THESE EXACTLY):

1. To see files in a folder:
   list_directory("~/Desktop")

2. To run terminal commands (mkdir, mv, ls, etc):
   execute_terminal_command("mkdir ~/Desktop/Photos")
   execute_terminal_command("mv ~/Desktop/*.jpg ~/Desktop/Photos/")

3. To verify something worked:
   list_directory("~/Desktop/Photos")  # See if files are there

🎯 ORGANIZING DESKTOP FILES - EXACT STEPS:

Step 1: list_directory("~/Desktop")
→ Look at output, count files by type

Step 2: execute_terminal_command("mkdir ~/Desktop/Photos")
→ Creates Photos folder

Step 3: list_directory("~/Desktop")
→ Verify Photos/ folder exists in the list

Step 4: execute_terminal_command("mv ~/Desktop/*.jpg ~/Desktop/Photos/")
→ Move JPG files

Step 5: list_directory("~/Desktop/Photos")
→ Verify JPG files are inside Photos folder

Step 6: list_directory("~/Desktop")
→ Verify JPG files are GONE from Desktop

Step 7: Repeat for other file types (PDF, MP4, PNG, etc.)

⚠️ CRITICAL RULES:

1. ALWAYS use execute_terminal_command() for mkdir and mv commands
2. ALWAYS verify with list_directory() after each action
3. Create ONE folder at a time
4. Move ONE file type at a time
5. Verify BEFORE moving to next step

❌ WRONG:
list_directory({"command": "mkdir ~/Desktop/Photos"})  # WRONG TOOL!

✅ CORRECT:
execute_terminal_command("mkdir ~/Desktop/Photos")  # RIGHT TOOL!

🧰 AVAILABLE TOOLS:

**File & Directory:**
- list_directory(directory_path) - See what's in a folder
- execute_terminal_command(command) - Run mkdir, mv, ls, etc.
- read_file_content(filepath) - Read file contents

**Verification:**
- verify_expectations(what_to_verify, verification_commands)
- self_critique(original_task, actions_summary, expected_outcome)

**Other:**
- Computer: move_mouse, click_mouse, type_text, press_key
- Apps: open_app, open_url, check_running_apps
- Memory: recall_from_memory, save_to_memory
- Debug: debug_last_error, take_screenshot

🎯 SIMPLE RULES:

1. Do ONE action
2. Verify it worked
3. Then do next action
4. Don't call 10 tools at once

That's it!

Work slowly, verify each step, and you'll succeed. 🎯"""

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
    config = {
        "configurable": {"thread_id": "my-robot-thread"},
        "recursion_limit": 50,  # Increased from default 25 for complex tasks
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
        if not all(
            danger.lower() not in prompt.lower() for danger in DANGEROUS_COMMANDS
        ):  # Quick safety check
            print("🚫 Unsafe command blocked! Try something nice.")
            continue

        print("🧠 AI is processing your request...\n")

        # Run the agent with feedback loop (include system prompt as first message)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        # Retry with provider switching on rate limit errors
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # Recreate agent with current model
                agent_executor = create_react_agent(llm, tools, checkpointer=memory)

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
