# FastAPI Frontend

This is a simple Next.js frontend designed to interact with a FastAPI backend for URL ingestion and question answering based on the ingested content.

## Getting Started

### Prerequisites

- Node.js and npm (or yarn) installed.
- Your FastAPI backend application running (typically on `http://localhost:8000`). Ensure CORS is configured in your FastAPI backend to accept requests from the frontend's origin (usually `http://localhost:9002` during development).

### Running the Frontend 


1.  **Install dependencies:**
    ```bash
    npm install
    # or
    # yarn install
    ```

2.  **Run the development server:**
    ```bash
    npm run dev
    # or
    # yarn dev
    ```
    This will typically start the Next.js application on `http://localhost:9002`.

3.  **Open your browser:**
    Navigate to `http://localhost:9002` (or the port specified in your terminal).

### Running the Backend (Example FastAPI Setup)

If you haven't set up your FastAPI backend yet, here's a minimal example assuming you have Python and pip installed:

1.  **Create a project directory for your backend and navigate into it.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3.  **Install FastAPI and Uvicorn:**
    ```bash
    pip install fastapi uvicorn "python-multipart" aiohttp beautifulsoup4 # Add other dependencies like sentence-transformers, faiss-cpu etc.
    ```
4.  **Create your main FastAPI file (e.g., `main.py`) with the necessary endpoints (`/ingest-url/`, `/ask-question/`, `/reset-embeddings/`) and CORS configuration.**

    *Example CORS setup in `main.py`:*
    ```python
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    origins = [
        "http://localhost:9002", # Your Next.js frontend origin
        "http://127.0.0.1:9002",
        # Add other origins if needed
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Define your endpoints here ---
    @app.post("/ingest-url/")
    async def ingest_url(url: str, max_depth: int = 1):
        # Your ingestion logic...
        print(f"Ingesting URL: {url} with max_depth: {max_depth}")
        # Replace with actual logic
        return {"message": f"Processing URL: {url}"}

    @app.post("/ask-question/")
    async def ask_question(question: str):
        # Your question answering logic...
        print(f"Received question: {question}")
        # Replace with actual logic
        return {"answer": f"Answer related to '{question}' based on ingested data."}

    @app.delete("/reset-embeddings/")
    async def reset_embeddings():
        # Your reset logic...
        print("Resetting embeddings...")
        # Replace with actual logic
        return {"message": "Embeddings reset"}

    # --- Add other endpoints and logic ---

    ```

5.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```

Now both your frontend and backend should be running, and you can use the frontend interface to interact with the backend API.
