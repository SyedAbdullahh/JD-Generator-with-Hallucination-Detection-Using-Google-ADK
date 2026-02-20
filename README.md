# Job Description Generation with Hallucination Detection using Google ADK

Multi-agent Job Description (JD) generation system built with Google ADK and deployable to Vertex AI Agent Engine.

## What this project does

- Accepts user requests related to JD generation.
- Routes in-scope requests through a manager pipeline.
- Generates a JD, checks it for hallucinations, and iteratively refines it.
- Uses an approval tool (`approve_jd`) to escalate when the JD is considered acceptable.
- Can be deployed as a remote reasoning engine on Vertex AI.

## Repository structure

- `agents/root_agent/agent.py`: top-level `root_agent` (`LlmAgent`) that delegates to `manager_agent`.
- `agents/manager_agent/agent.py`: `ManagerSequentialAgent` that stores `user_prompt` in session state and runs sub-agents sequentially.
- `agents/jd_generator_agent/agent.py`: generates initial JD and stores output in `state['curr_jd']`.
- `agents/anti_hallucination_loop/agent.py`: `LoopAgent` (`max_iterations=4`) over detector + refiner.
- `agents/hallucination_detector_agent/agent.py`: evaluates hallucination risk and stores feedback in `state['hallucination_detector_feedback']`.
- `agents/refiner_agent/agent.py`: improves JD formatting/content constraints and can call `approve_jd`.
- `tools/approve_jd.py`: tool that sets escalation (`tool_context._event_actions.escalate = True`).
- `utils/file_reader.py`: helper for loading prompt text files.
- `utils/special_file_reader.py`: dynamic instruction providers that inject `user_prompt` from state.
- `deployment/deploymentService.py`: deployment script for Vertex AI Agent Engine.
- `main.py`: placeholder script (not used for agent runtime).

## Agent flow

1. `root_agent` classifies incoming prompt:
	 - greetings / process questions -> answers directly
	 - JD generation request with enough details -> transfers to manager
	 - JD request with missing details -> asks follow-up questions
	 - out-of-scope -> declines politely
2. `manager_agent` stores initial user prompt in `ctx.session.state['user_prompt']`.
3. `jd_generator_agent` creates draft JD (`state['curr_jd']`).
4. `anti_hallucination_agent` loop runs:
	 - `hallucination_detector_agent` assesses hallucination status
	 - `refiner_agent` refines JD and approves when appropriate
5. Loop stops on escalation/approval or when max iterations are reached.

## Prerequisites

- Python `>= 3.11`
- Google Cloud project with Vertex AI enabled
- Authenticated Google Cloud credentials (ADC)
- A writable GCS staging bucket

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in repo root with:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_CLOUD_STAGING_BUCKET=gs://your-staging-bucket
```

## Local usage notes

- This repo currently does **not** provide a dedicated local runner script for chat interaction.
- `main.py` is only a placeholder (`Hello from adk-poc!`).
- Use your ADK-compatible local runner/tooling to load `agents/root_agent/agent.py` if you want local interactive testing.

## Deploy to Vertex AI Agent Engine

Run:

```bash
python deployment/deploymentService.py
```

What it does:

- Initializes Vertex AI from `.env`
- Wraps `root_agent` in `reasoning_engines.AdkApp`
- Deploys with required packages and local extra packages (`./agents`, `./utils`, `./tools`)

On success it prints the deployed resource name.

## Query deployed agent (stream)

Example request shape:

```bash
curl -N \
	-H "Authorization: Bearer $ACCESS_TOKEN" \
	-H "Content-Type: application/json" \
	"https://us-central1-aiplatform.googleapis.com/v1/projects/<PROJECT_ID>/locations/us-central1/reasoningEngines/<ENGINE_ID>:streamQuery" \
	-d '{
				"input": {
					"message": "give me JD for BD at WAMO Labs DHA Lahore",
					"user_id": "user-1"
				}
			}'
```

## Prompt and policy behavior to be aware of

- JD generator prompt may infer missing fields (including location/company details) when user input is sparse.
- Hallucination detector/refiner prompts attempt to block unsupported specifics.
- Because these prompts are strict, quality and acceptance can vary with prompt detail.
- Approval is represented by escalation action in tool context.

## Evaluation artifacts

The root agent folder contains eval sets used for ADK evaluations:

- `agents/root_agent/evalseta8c913.evalset.json`
- `agents/root_agent/evalseteaec99.evalset.json`

## Dependencies

From `requirements.txt`:

- `google-cloud-aiplatform[adk,agent_engines]`
- `google-adk`
- `google-generativeai`
- `python-dotenv`
- `pydantic`

## Current limitations

- No explicit tests in repository.
- No local CLI command wrapper included in repo.
- Some agent metadata files (`description.txt`) are empty (e.g., root agent).

