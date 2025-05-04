from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application factory function
def create_app() -> FastAPI:
    """
    Creates and configures a FastAPI application instance.
    """
    app = FastAPI(
        title="Scrapper Bot",
        description=(
            "Scrapper Bot is a web scraping and question-answering service powered by FastAPI, "
            "OpenAI's GPT models, and PGVector for vector-based storage and retrieval."
        ),
        version="1.0.0"
    )

    # Configure CORS (optional, can be adjusted based on your requirements)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for now. Restrict in production.
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router)

    # Root endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to Scrapper Bot! Use the API to scrape websites, store embeddings, and ask questions."}

    return app


# Main entry point
app = create_app()

if __name__ == "__main__":
    logger.info("Starting Scrapper Bot server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)