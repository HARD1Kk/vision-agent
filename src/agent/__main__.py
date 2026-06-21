from agent.graph import app
from agent.state import AgentState


def main():
    # This task is engineered to trigger every condition in your Executor
    comprehensive_test_task = (
        "1. Press the 'win' key to open the start menu and search for your web browser, then press 'enter' to open it. "
        "2. Wait 3 seconds for the browser to fully load. "
        "3. Type 'en.wikipedia.org' and press enter. "
        "4. Scroll down the page once. "
        "5. Use the hotkey 'ctrl+a' to select all text on the screen, then use the hotkey 'ctrl+c' to copy it. "
        "6. Press the 'win' key, type 'notepad', and press enter to open Notepad. "
        "7. Click inside the empty Notepad window, use the hotkey 'ctrl+v' to paste the text. "
        "8. Use the hotkey 'ctrl+s' to save the file."
    )

    initial_state: AgentState = {
        "task": comprehensive_test_task,
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
