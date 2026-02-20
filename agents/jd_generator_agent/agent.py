from google.adk.agents import LlmAgent
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so sibling packages like `utils`
# (which live next to `agents/`) can be imported when this module is loaded
# from the ADK runner which sets its CWD to the `agents` directory.
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from utils.file_reader import read_file



jd_generator_agent = LlmAgent(
    name="jd_generator_agent",
    model='gemini-2.5-flash',
    description=read_file(Path(__file__).with_name("description.txt")),
    instruction=read_file(Path(__file__).with_name("instructions.txt")),
    output_key="curr_jd"
)
