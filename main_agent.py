from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from agent_tools import (
    move_mouse, click_mouse, search_file, open_app, open_url, 
    execute_terminal_command, take_screenshot, get_screen_info,
    check_running_apps, type_text, press_key, get_current_directory,
    read_file_content, DANGEROUS_COMMANDS
)
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

# AGENTIC AI SYSTEM PROMPT - Guides autonomous behavior
SYSTEM_PROMPT = """You are an autonomous AI agent that controls a computer to accomplish user goals.

🎯 YOUR CAPABILITIES:
- Computer control (mouse, keyboard, apps, terminal)
- Self-debugging and error recovery
- Planning multi-step tasks autonomously
- Learning from failures and adapting approach

🧠 AGENTIC BEHAVIOR GUIDELINES:

1. **THINK BEFORE YOU ACT**
   - Break complex tasks into logical steps
   - Plan your approach before executing
   - Consider what could go wrong

2. **BE AUTONOMOUS**
   - Don't ask for permission - take action
   - If something fails, debug and try alternative approaches
   - Use tools to inspect the system state when unsure

3. **DEBUG YOURSELF**
   - If a tool fails, use get_screen_info(), check_running_apps(), or take_screenshot() to investigate
   - Read error messages carefully and adjust your approach
   - Try alternative methods if the first approach doesn't work

4. **VERIFY YOUR ACTIONS**
   - After important actions, verify they succeeded
   - Use check_running_apps() to confirm apps opened
   - Use get_screen_info() to verify mouse position
   - Take screenshots when debugging UI issues

5. **BE VERBOSE**
   - Explain your reasoning clearly
   - Share your plan before executing
   - Reflect on what worked and what didn't

6. **LEARN FROM ERRORS**
   - If command fails, analyze why and try a different approach
   - Use execute_terminal_command() for system tasks
   - Combine tools creatively to solve problems

AVAILABLE TOOLS:
- Mouse: move_mouse, click_mouse
- Keyboard: type_text, press_key
- System: execute_terminal_command, get_current_directory
- Apps: open_app, open_url, check_running_apps
- Files: search_file, read_file_content
- Debugging: get_screen_info, take_screenshot

Remember: You are autonomous. Take initiative, debug yourself, and accomplish the goal through any means necessary (safely)."""

# List of all tools
tools = [
    move_mouse, click_mouse, type_text, press_key,
    search_file, open_app, open_url, check_running_apps,
    execute_terminal_command, get_current_directory, read_file_content,
    take_screenshot, get_screen_info
]

# The AI brain with agentic system prompt
llm = ChatOllama(model="llama3.1:8b")

# Memory to remember past actions (helps with feedback)
memory = MemorySaver()

# The agent with built-in loop for feedback and errors + agentic system prompt
agent_executor = create_react_agent(
    llm, 
    tools, 
    checkpointer=memory
)

# Config for the session (like a conversation ID)
config = {"configurable": {"thread_id": "my-robot-thread"}}

# Create a prompt session with history support for arrow key navigation
session = PromptSession(history=InMemoryHistory())

print("="*70)
print("🤖 AGENTIC AI ROBOT - AUTONOMOUS COMPUTER CONTROL SYSTEM")
print("="*70)
print("\n🎯 I'm an autonomous AI that can:")
print("   • Control your computer (mouse, keyboard, apps)")
print("   • Execute terminal commands safely")
print("   • Debug myself and recover from errors")
print("   • Plan and execute multi-step tasks")
print("   • Learn from failures and adapt")
print("\n💡 Tips:")
print("   • Give me complex tasks - I'll break them down myself")
print("   • If I fail, I'll debug and try different approaches")
print("   • Use ↑↓ arrow keys for command history")
print("   • Type 'exit' to quit")
print("\n📋 Example commands:")
print("   • 'Create a new folder called test_project on Desktop'")
print("   • 'Open Chrome, go to YouTube, and search for AI tutorials'")
print("   • 'Take a screenshot and tell me the screen size'")
print("   • 'Find all Python files in my home directory'")
print("="*70 + "\n")

while True:
    try:
        prompt = session.prompt("🤖 Your command: ")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")
        break
    if prompt.lower() == 'exit':
        print("👋 Goodbye!")
        break
    if not all(danger.lower() not in prompt.lower() for danger in DANGEROUS_COMMANDS):  # Quick safety check
        print("🚫 Unsafe command blocked! Try something nice.")
        continue

    print("🧠 AI is processing your request...\n")
    
    # Run the agent with feedback loop (include system prompt as first message)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    for chunk in agent_executor.stream({"messages": messages}, config):
        # Show agent node execution
        if "agent" in chunk:
            messages = chunk["agent"]["messages"]
            for msg in messages:
                # AI thinking/response
                if hasattr(msg, 'content') and msg.content:
                    print(f"💭 AI Thinking: {msg.content}")
                
                # Tool calls
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.get('name', 'unknown')
                        tool_args = tool_call.get('args', {})
                        print(f"🔧 Calling Tool: {tool_name}({tool_args})")
        
        # Show tool execution results
        if "tools" in chunk:
            messages = chunk["tools"]["messages"]
            for msg in messages:
                if hasattr(msg, 'content'):
                    print(f"✅ Tool Result: {msg.content}")
    
    print("\n✨ Task completed!\n")