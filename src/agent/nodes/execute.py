from agent.executor import Executor
from agent.models import ActionType
from agent.state import AgentState

executor = Executor()


def execute_action_node(state: AgentState):
    print(f"⚙️ Executing step {state.get('step', 0)}...")

    # 1. READ FROM STATE
    current_action = state.get("action")
    current_step = state.get("step", 0)

    if current_action is None:
        return {"history": ["Error: No action provided to execute."]}

    # 2. DO THE WORK
    try:
        # Pass the Action object directly to your class method
        result_log = executor.execute_action(current_action)
    except Exception as e:
        # Catches PyAutoGUI failsafes or coordinate math errors
        result_log = f"Execution failed: {str(e)}"

    # 3. CHECK FOR COMPLETION
    # Using the ActionType enum you defined in your models
    is_done = current_action.action == ActionType.DONE

    # 4. UPDATE THE STATE
    return {
        "step": current_step + 1,
        "done": is_done,
        "history": [f"Step {current_step}: {result_log}"],
    }
