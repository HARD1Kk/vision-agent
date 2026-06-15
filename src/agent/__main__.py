from agent.graph import app
from agent.state import AgentState


def main():
    initial_state: AgentState = {
        "task": "Open notepad and write 'Hello' ",
        "screenshot": None,
        "action": None,
        "reasoning": "",
        "step": 1,
        "done": False,
        "history": ["Agent initialized."],
    }

    print("🚀 Launching Desktop OS Agent...")

    # Run the graph end-to-end
    app.invoke(initial_state)


if __name__ == "__main__":
    main()
