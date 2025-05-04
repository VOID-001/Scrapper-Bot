from services.vectorstore import VectorDB
from utils.text_utils import clean_text
from openai import OpenAI
from config import OPENAI_API_KEY
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Use DEBUG for detailed logs
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def ingest_and_store(content: str, url: str):
    """
    Ingests text content, generates embeddings using OpenAI's API, and stores them in the vector database.
    """
    try:
        logger.info("Started ingestion process for URL: %s", url)

        # Step 1: Clean the text content
        logger.debug("Cleaning text content...")
        cleaned_text = clean_text(content)
        logger.debug("Cleaned text: %s", cleaned_text[:100])  # Log first 100 characters

        # Step 2: Generate embeddings using OpenAI's embedding model
        logger.debug("Generating embeddings for the content...")
        embeddings = client.embeddings.create(input=[cleaned_text], model="text-embedding-ada-002").data[0].embedding
        logger.debug("Generated embedding (length: %d, first 5 dimensions): %s", len(embeddings), embeddings[:5])

        # Step 3: Store embeddings in the vector database
        logger.debug("Connecting to the vector database for storage...")
        db = VectorDB()
        logger.debug("Storing embeddings into the database...")
        db.insert_vector(url=url, embedding=embeddings, content=cleaned_text)
        logger.info("Successfully stored content and embeddings for URL: %s", url)
        db.close()

    except Exception as e:
        logger.error("Error during ingestion and storage for URL %s: %s", url, e, exc_info=True)
        raise


def ask_question(question: str, top_k: int = 3):
    """
    Retrieves the most relevant answers to a question from the vector database using both:
    1. Vector similarity search.
    2. LLM-based search.

    Args:
        question (str): The question to ask.
        top_k (int): Number of top similar results to return. Default is 3.

    Returns:
        dict: A dictionary containing results from vector similarity and LLM-based search.
    """
    try:
        logger.info("Processing question: %s", question)

        # Step 1: Generate embedding for the question
        logger.debug("Generating embedding for the question...")
        question_embedding = client.embeddings.create(input=[question], model="text-embedding-ada-002").data[0].embedding
        logger.debug("Question embedding (length: %d, first 5 dimensions): %s", len(question_embedding), question_embedding[:5])

        # Step 2: Query the vector database for similar content
        logger.debug("Querying the vector database for similar content...")
        db = VectorDB()
        vector_results = db.query_similar(question_embedding, top_k=top_k)

        # Enhance vector similarity with content snippets
        enhanced_results = []
        for result in vector_results:
            content_snippet = db.get_content_snippet(result["id"])
            enhanced_results.append({
                "id": result.get("id"),
                "url": result.get("url"),
                "similarity": round(result.get("similarity", 0.0), 2),
                "snippet": content_snippet
            })

        db.close()

        logger.info("Vector similarity results retrieved: %d records", len(enhanced_results))
        logger.debug("Enhanced Similarity Results: %s", enhanced_results)

        # Step 3: Use LLM to retrieve richer answers
        logger.debug("Retrieving answers using LLM-based search...")
        llm_results = []
        for result in enhanced_results:
            try:
                llm_query = f"Based on the following content, answer the question: {question}\n\nContent: {result.get('snippet') or result.get('url')}"
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": llm_query}
                    ],
                    max_tokens=150
                )
                llm_results.append({
                    "id": result.get("id"),
                    "url": result.get("url"),
                    "answer": response.choices[0].message.content.strip(),
                    "similarity": result.get("similarity")
                })
                logger.debug(
                    "LLM Result - ID: %s, URL: %s, Answer: %s",
                    result.get("id"), result.get("url"), response.choices[0].message.content.strip()
                )
            except Exception as e:
                logger.error("Error during LLM processing for result ID %s: %s", result.get("id"), e, exc_info=True)

        logger.info("LLM-based search results retrieved successfully.")

        return {"vector_similarity": enhanced_results, "llm_search": llm_results}

    except Exception as e:
        logger.error("Error during question answering: %s", e, exc_info=True)
        raise