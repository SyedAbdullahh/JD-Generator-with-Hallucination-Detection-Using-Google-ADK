from google.adk.agents import SequentialAgent, LlmAgent
from agents.jd_generator_agent.agent import jd_generator_agent
from agents.anti_hallucination_loop.agent import anti_hallucination_agent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

# Wrap SequentialAgent to store user query in state
class ManagerSequentialAgent(SequentialAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # 1️⃣ Store the original user query in state
        if ctx.user_content and ctx.user_content.parts:
            # Store the original user query in the session state so it is
            # available to sub-agents via ReadonlyContext (ctx.session.state).
            ctx.session.state["user_prompt"] = ctx.user_content.parts[0].text

        # 2️⃣ Run normal sequential execution
        async for event in super()._run_async_impl(ctx):
            yield event

# Instantiate root agent with wrapped class
manager_agent = ManagerSequentialAgent(
    name="manager_agent",
    sub_agents=[jd_generator_agent, anti_hallucination_agent]
)


