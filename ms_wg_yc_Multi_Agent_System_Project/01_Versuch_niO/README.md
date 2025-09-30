# Multi-Agent Lab Template

This repository provides the summer-school starter kit for building a multi-agent AI system that turns natural language feature requests into structured documentation. The template boots quickly, showcases a LangGraph + Chainlit integration, and leaves dedicated extension points for students to implement agent logic.

## Quick Start

```bash
# Clone and enter the project
git clone <repository-url> multi-agent-lab
cd multi-agent-lab

# Install dependencies with UV
uv sync

# Provide API keys for your LLM provider (OpenRouter powers the default chat)
cp .env.example .env
# edit .env with OPENROUTER_API_KEY and optional referer/title metadata

# Launch the Chainlit playground
uv run chainlit run src/main.py --watch
```

Open http://localhost:8000 and send a feature idea. With an `OPENROUTER_API_KEY` configured the workflow streams the conversation through LangGraph + OpenRouter's `openrouter/sonoma-sky-alpha` model; otherwise it falls back to a local echo responder while preserving uploads under `outputs/uploads`.

## Repository Layout

```
src/
├── main.py              # Chainlit entry point wired to LangGraph
├── agents/              # Student-implemented agent stubs
├── workflows/           # Example graph + state definitions
└── utils/               # File helpers and logging setup
outputs/                 # Generated artefacts (sessions, logs, docs)
examples/                # Sample prompts and scenarios
docs/                    # Student-facing guides
specs/                   # Spec-driven development artefacts
tests/                   # Test suite scaffolding
```

Key documentation lives under `specs/001-i-want-to/`:
- `spec.md` – business requirements
- `research.md` – stack decisions and rationale
- `tasks.md` – dependency-ordered implementation plan
- `quickstart.md` – 15-minute student onboarding flow

## Development Workflow

- Add dependencies with `uv add <package>` (use `--dev` for tooling).
- Run the Chainlit app during development: `uv run chainlit run src/main.py --watch`.
- Persist documents or artefacts using helpers in `src/utils/file_utils.py`.
- Log debug information with the central logger from `src/utils/logging.py`.

## Current Capabilities

- Chat interface with session tracking, upload persistence, and OpenRouter-powered replies (with a safe echo fallback when no key is provided).
- LangGraph workflow compiled via `build_chat_workflow()` that accepts message-state inputs and emits AI messages.
- Agent modules scaffolded with async `run` methods awaiting student logic.
- Outputs directory structured for downstream document generation.

## Student Extension Points

1. Replace the baseline chat node with a supervisor graph that coordinates the agent suite.
2. Fill in the agent stubs to produce requirements, technical analyses, and testing plans.
3. Expand `docs/` with learning exercises and update `examples/` with domain scenarios.
4. Add contract, integration, and regression tests in the `tests/` folder.

Happy building!
