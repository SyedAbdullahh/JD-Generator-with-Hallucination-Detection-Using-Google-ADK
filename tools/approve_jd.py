from google.adk.tools.tool_context import ToolContext

def approve_jd(tool_context:ToolContext):
    tool_context._event_actions.escalate=True
    return {}