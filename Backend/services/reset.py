from psycopg2 import connect
from config import PGVECTOR_HOST, PGVECTOR_PORT, PGVECTOR_DB, PGVECTOR_USER, PGVECTOR_PASSWORD
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def clear_embeddings():
    """
    Clears all data in the 'scraptable' table.
    """
    try:
        logger.info("Connecting to PGVector database to clear embeddings...")
        conn = connect(
            host=PGVECTOR_HOST,
            port=PGVECTOR_PORT,
            database=PGVECTOR_DB,
            user=PGVECTOR_USER,
            password=PGVECTOR_PASSWORD
        )
        cursor = conn.cursor()

        # Clear the table
        logger.debug("Executing SQL to clear 'scraptable' table...")
        cursor.execute("TRUNCATE TABLE scraptable;")
        conn.commit()

        logger.info("All embeddings cleared from 'scraptable' table successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error("Failed to clear embeddings: %s", e, exc_info=True)
        raise