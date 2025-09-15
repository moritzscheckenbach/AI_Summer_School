# summerschool-2025
This project contains the lab exercises for 2025 summerschool of University of applied sciences Karlsruhe

## Quickstart (uv)

1.  Install uv: https://docs.astral.sh/uv/
2.  Install dependencies:

```bash
uv sync
```

3.  Run backend (FastAPI) in your first terminal:

```bash
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

4.  Run UI (Streamlit multipage app) in your second terminal:

```bash
BACKEND_URL=http://localhost:8000 uv run streamlit run ui/Home.py \
  --server.showEmailPrompt false \
  --server.runOnSave true
```

-   Open the UI at http://localhost:8501
-   The backend is available at http://localhost:8000 (health check: `/healthz`)

## Structure

-   `backend/`: FastAPI app with routers for each day: `/api/day{1..5}/...`
-   `ui/`: Streamlit multipage app with `Home.py` and page files in `ui/pages/`
    -   Day 1–2: Use a simple single-message input.
    -   Day 3–5: Use a full chat interface.

See Streamlit's documentation for more info: [st.chat_input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)

## Implementing the Exercises

This repository provides a pre-built FastAPI backend and a Streamlit UI so you can focus on the core logic of the exercises.

### Workflow

For each day, your main task is to **implement the logic inside the backend**. The UI is already connected to the backend endpoints. You will replace the stub/echo logic with your solutions.

### Where to Add Your Code

-   **Backend Logic**: All exercise implementations go into the `backend/routers/` directory. Each day has its own file:
    -   **Day 1**: Open `backend/routers/day1.py` and implement the multilingual film critic, sentiment classifier, etc.
    -   **Day 2**: Open `backend/routers/day2.py` for Self-Consistency, Tool-Use, and Plan-and-Solve.
    -   **Day 3**: Open `backend/routers/day3.py` for the Basic RAG implementation.
    -   **Day 4**: Open `backend/routers/day4.py` for the Advanced RAG agent.
    -   **Day 5**: Open `backend/routers/day5.py` for the open-domain agent.

-   **Data Models**: For tasks requiring structured data (like the Day 1 sentiment classifier), you may need to define or modify Pydantic models in `backend/models.py`.

-   **UI (Optional)**: The UI is located in `ui/pages/`. You generally **do not need to change the UI code**. It is set up to call the correct backend endpoint for each day. You can inspect the code to see how the frontend calls your backend code.
