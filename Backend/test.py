import logging
from services.vectorstore import VectorDB

# Configure logging to display each operation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rag_pipeline():
    """
    Tests the RAG pipeline by embedding a specific text and storing it in the vector database.
    """
    # Test data
    test_text = "Happy birthday VOID 10th dec"
    fake_embedding = [0.1] * 1536  # Simulated dummy embedding (size matches OpenAI embedding model)

    try:
        # Step 1: Connect to the vector database
        logger.info("Connecting to the vector database...")
        db = VectorDB()

        # Step 2: Insert the test text and fake embedding into the database
        logger.info(f"Inserting test data into the database...")
        db.insert_vector(url="test://localhost", embedding=fake_embedding, content=test_text)

        # Step 3: Query the database for the most similar results
        logger.info("Querying the database for similar texts...")
        results = db.query_similar(embedding=fake_embedding, top_k=1)

        # Step 4: Display results
        logger.info("Query Results:")
        for result in results:
            logger.info(f"ID: {result['id']}, URL: {result['url']}, Content: {result['content']}, Similarity: {result['similarity']}")

        # Close the connection
        db.close()
    except Exception as e:
        logger.error(f"An error occurred during the test: {e}")

if __name__ == "__main__":
    logger.info("Starting RAG pipeline test...")
    test_rag_pipeline()