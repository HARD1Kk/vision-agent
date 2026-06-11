import operator

from PIL import Image
from typing_extensions import Annotated, TypedDict

from agent.models import Action


# Initialise state
class AgentState(TypedDict):
    task: str
    screenshot: Image.Image | None
    action: Action | None
    reasoning: str
    step: int
    done: bool
    history: Annotated[list[str], operator.add]


# def take_screenshot_node(state: AgentState):
#     # 1. READ FROM STATE (Optional):
#     # For example, let's print the task to know what we are taking a screenshot for
#     print(f"Taking screenshot for task: {state.get('task')}")

#     # 2. DO THE WORK:
#     new_image = capture_image()

#     # 3. UPDATE THE STATE:
#     # Return a dictionary with the exact names of the fields you want to update.
#     # We will update the 'screenshot' field, and let's add a note to our 'history'.
#     return {"screenshot": new_image, "history": ["Took a new screenshot."]}


# client = genai.Client()
# brain = GeminiBrain(client=client, model=settings.MODEL)

# executor = Executor()


# def analyze_screenshot_node(state: AgentState):
#     print("🧠 Brain is analyzing the screen...")

#     # 1. READ FROM STATE
#     current_task = state.get("task")
#     current_screenshot = state.get("screenshot")
#     current_history = state.get("history")

#     # Safety check
#     if not current_screenshot:
#         return {"history": ["Error: No screenshot provided to brain."]}

#     # 2. DO THE WORK (Hand off to your class)

#     decision = brain.decide_action(
#         task=current_task, screenshot=current_screenshot, history=current_history
#     )

#     # 3. UPDATE THE STATE
#     # We update the 'action' field, and append a log to the history
#     return {"action": decision, "history": [f"Brain decided to: {decision}"]}


# def execute_action_node(state: AgentState):
#     print(f"⚙️ Executing step {state.get('step', 0)}...")

#     # 1. READ FROM STATE
#     current_action = state.get("action")
#     current_step = state.get("step", 0)

#     if current_action is None:
#         return {"history": ["Error: No action provided to execute."]}

#     # 2. DO THE WORK
#     try:
#         # Pass the Action object directly to your class method
#         result_log = executor.execute_action(current_action)
#     except Exception as e:
#         # Catches PyAutoGUI failsafes or coordinate math errors
#         result_log = f"Execution failed: {str(e)}"

#     # 3. CHECK FOR COMPLETION
#     # Using the ActionType enum you defined in your models
#     is_done = current_action.action == ActionType.DONE

#     # 4. UPDATE THE STATE
#     return {
#         "step": current_step + 1,
#         "done": is_done,
#         "history": [f"Step {current_step}: {result_log}"],
#     }
