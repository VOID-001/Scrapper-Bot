from fastapi import APIRouter, HTTPException
from services.scraper import Scraper
from services.rag import ask_question
from services.reset import clear_embeddings

router = APIRouter()

@router.post("/ingest-url/")
async def ingest_url(url: str, max_depth: int = 1):
    """
     Endpoint to enter the URL to be scraped .
     """
    try:
        scraper = Scraper(base_url=url, max_depth=max_depth)
        scraper.scrape()
        return {"message": "URL processed successfully!", "result": "Data stored in pgvector > scraptable > embedding"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask-question/")
async def ask_question_endpoint(question: str):
    """
    Endpoint to ask questions based on the scraped and embedded content.
    """
    try:
        answer = ask_question(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset-embeddings/")
async def reset_embeddings():
    """
    Endpoint to clear all data in the embeddings table.
    """
    try:
        clear_embeddings()
        return {"status": "success", "message": "All embeddings have been cleared."}
    except Exception as e:
        return {"status": "error", "message": str(e)}