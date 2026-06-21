from groq import Groq

from agent.core.config import settings
from agent.executor import Executor
from agent.llm import GroqBrain
from agent.state import AgentState

client = Groq(api_key=settings.GROQ_API_KEY)

brain = GroqBrain(
    client=client, vision_model=settings.VISION_MODEL, logic_model=settings.LOGIC_MODEL
)
executor = Executor()


def analyze_screenshot_node(state: AgentState):
    print("🧠 Brain is analyzing the screen...")

    # 1. READ FROM STATE
    current_task = state.get("task")
    current_screenshot = state.get("screenshot")
    current_history = state.get("history", [])  # Default to empty list if missing

    # Safety check
    if not current_screenshot:
        return {"history": ["Error: No screenshot provided to brain."]}

    # 2. DO THE WORK (This handles both Vision and Logic passes internally)
    decision = brain.decide_action(
        task=current_task, screenshot=current_screenshot, history=current_history
    )

    # 3. FORMAT THE LOG FOR HISTORY
    # Extracting details from the Pydantic model for a clean log
    log_entry = (
        f"Action: {decision.action.upper()} "
        f"| Coords: ({decision.x}, {decision.y}) "
        f"| Text: '{decision.text}' "
        f"| Reasoning: {decision.reasoning}"
    )
    print(f"✅ {log_entry}")

    # 4. UPDATE THE STATE
    return {
        "action": decision,
        "history": [log_entry],  # Append the clean log to state history
    }
