from google.adk.agents import LlmAgent
import sys
from pathlib import Path
from tools.approve_jd import approve_jd

# Ensure project root on sys.path so `utils` package (sibling of `agents`)
# can be imported when ADK sets CWD to `agents/`.
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from utils.file_reader import read_file
from utils.special_file_reader import checker_instruction_provider_r


refiner_agent = LlmAgent(
    name='refiner_agent',
    model='gemini-2.5-flash',
    instruction=checker_instruction_provider_r,
    tools=[approve_jd],
    description=read_file(Path(__file__).with_name("description.txt"))
)