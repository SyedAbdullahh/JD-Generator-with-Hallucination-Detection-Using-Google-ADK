from pathlib import Path
import sys
from google.adk.agents import SequentialAgent, LlmAgent
from agents.manager_agent.agent import manager_agent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from utils.file_reader import read_file



# Instantiate root agent with wrapped class
root_agent = LlmAgent(
    name="root_agent",
    instruction=read_file(Path(__file__).with_name("instructions.txt")),
    description=read_file(Path(__file__).with_name("description.txt")),
    sub_agents=[manager_agent]
)


