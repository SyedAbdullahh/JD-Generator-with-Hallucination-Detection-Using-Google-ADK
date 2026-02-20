from google.adk.agents import LoopAgent
from agents.hallucination_detector_agent.agent import hallucination_detector
from agents.refiner_agent.agent import refiner_agent


anti_hallucination_agent=LoopAgent(
    name="anti_hallucination_agent",
    sub_agents=[hallucination_detector,refiner_agent],
    max_iterations=4
)