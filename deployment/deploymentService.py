from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from agents.root_agent.agent import root_agent
from dotenv import load_dotenv
from vertexai import init
import os


def create() -> None:
    """Creates a new deployment."""
    load_dotenv()

    init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
        staging_bucket=os.environ["GOOGLE_CLOUD_STAGING_BUCKET"], 
    )
    # First wrap the agent in AdkApp
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    # Now deploy to Agent Engine
    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
            "google-adk",
            "google-generativeai",
            "python-dotenv",
            "pydantic"
        ],
        extra_packages=["./agents", "./utils", "./tools"],
    )
    print(f"Created remote app: {remote_app.resource_name}")


if __name__ == "__main__":
    create()