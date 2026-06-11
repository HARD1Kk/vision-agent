from groq import Groq

from agent.core.config import settings
from agent.executor import Executor
from agent.llm import GroqBrain
from agent.state import AgentState

client = Groq(api_key=settings.GROQ_API_KEY)
brain = GroqBrain(client=client, model=settings.MODEL)
executor = Executor()


def analyze_screenshot_node(state: AgentState):
    print("🧠 Brain is analyzing the screen...")

    # 1. READ FROM STATE
    current_task = state.get("task")
    current_screenshot = state.get("screenshot")
    current_history = state.get("history")

    # Safety check
    if not current_screenshot:
        return {"history": ["Error: No screenshot provided to brain."]}

    # 2. DO THE WORK (Hand off to your class)

    decision = brain.decide_action(
        task=current_task, screenshot=current_screenshot, history=current_history
    )

    # 3. UPDATE THE STATE
    # We update the 'action' field, and append a log to the history
    return {"action": decision, "history": [f"Brain decided to: {decision}"]}
