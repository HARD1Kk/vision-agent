from agent.graph import app
from agent.state import AgentState

initial_state: AgentState = {
    "task": "Open Notepad and type 'Hello World'",
    "screenshot": None,
    "action": None,
    "reasoning": "",
    "step": 1,
    "done": False,
    "history": ["Agent initialized."],
}

print("🚀 Launching Desktop OS Agent...")

# Run the graph end-to-end
final_state = app.invoke(initial_state)

print("\n--- EXECUTION SUMMARY ---")
for log in final_state["history"]:
    print(log)
