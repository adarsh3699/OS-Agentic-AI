from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from agent_tools import move_mouse, click_mouse, search_file, open_app  # Import your tools
from agent_tools import open_url

# List of all tools
tools = [move_mouse, click_mouse, search_file, open_app, open_url]

# The AI brain
llm = ChatOllama(model="llama3.1:8b")

# Memory to remember past actions (helps with feedback)
memory = MemorySaver()

# The agent with built-in loop for feedback and errors
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

# Config for the session (like a conversation ID)
config = {"configurable": {"thread_id": "my-robot-thread"}}

print("Your AI Robot is ready! Type a command like 'Move mouse to 500,300 and click left'. Type 'exit' to stop.")

while True:
    prompt = input("\n🤖 Your command: ")
    if prompt.lower() == 'exit':
        print("👋 Goodbye!")
        break
    if not all(danger.lower() not in prompt.lower() for danger in ['rm -rf', 'sudo rm']):  # Quick safety check
        print("🚫 Unsafe command blocked! Try something nice.")
        continue

    print("🧠 AI is processing your request...\n")
    
    # Run the agent with feedback loop
    for chunk in agent_executor.stream({"messages": [{"role": "user", "content": prompt}]}, config):
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