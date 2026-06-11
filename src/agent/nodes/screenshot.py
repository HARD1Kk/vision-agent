from agent.screen import capture_image
from agent.state import AgentState


def take_screenshot_node(state: AgentState):
    # 1. READ FROM STATE (Optional):
    # For example, let's print the task to know what we are taking a screenshot for
    print(f"Taking screenshot for task: {state.get('task')}")

    # 2. DO THE WORK:
    new_image = capture_image()

    # 3. UPDATE THE STATE:
    # Return a dictionary with the exact names of the fields you want to update.
    # We will update the 'screenshot' field, and let's add a note to our 'history'.
    return {"screenshot": new_image, "history": ["Took a new screenshot."]}
