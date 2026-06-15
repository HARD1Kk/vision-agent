from IPython.display import Image, display
from langgraph.graph import END, START, StateGraph

from agent.nodes.analyze import analyze_screenshot_node
from agent.nodes.execute import execute_action_node
from agent.nodes.screenshot import take_screenshot_node
from agent.state import AgentState

# 1. Initialize the StateGraph with your schema
workflow = StateGraph(AgentState)

# 2. Register your nodes
workflow.add_node("screenshot_step", take_screenshot_node)
workflow.add_node("analyze_step", analyze_screenshot_node)
workflow.add_node("execute_step", execute_action_node)

# 3. Define the linear connections
workflow.add_edge(START, "screenshot_step")
workflow.add_edge("screenshot_step", "analyze_step")
workflow.add_edge("analyze_step", "execute_step")


# 4. Define the conditional loop router
def should_continue(state: AgentState) -> str:
    """Evaluates whether the graph should loop or terminate."""
    # Check the flag set by your executor node
    if state.get("done"):
        print("🏁 Task complete! Exiting graph.")
        return END

    # If not done, loop back to the beginning to verify the result of the action
    print("🔄 Action executed. Looping back for a new screenshot...")
    return "screenshot_step"


# 5. Attach the conditional edge to the execution node
workflow.add_conditional_edges("execute_step", should_continue)

# 6. Compile the workflow into an executable application
app = workflow.compile()

# Display the PNG image directly
display(Image(app.get_graph().draw_mermaid_png()))
