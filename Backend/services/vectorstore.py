import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
from config import PGVECTOR_HOST, PGVECTOR_PORT, PGVECTOR_DB, PGVECTOR_USER, PGVECTOR_PASSWORD
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):

        try:
            logger.debug("Connecting to PGVector database...")
            self.conn = psycopg2.connect(
                host=PGVECTOR_HOST,
                port=PGVECTOR_PORT,
                database=PGVECTOR_DB,
                user=PGVECTOR_USER,
                password=PGVECTOR_PASSWORD
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            logger.info("Connected to PGVector database successfully!")
            self._ensure_table_exists()
        except Exception as e:
            logger.error("Failed to connect to the database: %s", e)
            raise

    def _ensure_table_exists(self):
        """
        Ensures the 'scraptable' table and the unique constraint on the 'url' column exist.
        """
        try:
            logger.debug("Ensuring 'scraptable' table exists...")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS scraptable (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                embedding VECTOR(1536) NOT NULL,
                content TEXT NOT NULL
            );
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            logger.info("'scraptable' table ensured to exist.")

            logger.debug("Ensuring 'url' column has UNIQUE constraint...")
            # Check if the unique constraint already exists
            check_constraint_query = """
            SELECT conname
            FROM pg_constraint
            WHERE conname = 'unique_url';
            """
            self.cursor.execute(check_constraint_query)
            result = self.cursor.fetchone()

            if not result:
                logger.debug("Adding UNIQUE constraint to 'url' column...")
                add_unique_constraint_query = """
                ALTER TABLE scraptable
                ADD CONSTRAINT unique_url UNIQUE (url);
                """
                self.cursor.execute(add_unique_constraint_query)
                self.conn.commit()
                logger.info("UNIQUE constraint on 'url' column added successfully.")
            else:
                logger.info("UNIQUE constraint on 'url' column already exists.")
        except Exception as e:
            logger.error("Failed to ensure 'scraptable' table or constraints exist: %s", e)
            self.conn.rollback()
            raise

    def insert_vector(self, url: str, embedding: list, content: str):
        """
        Inserts a new record into the 'scraptable' table if the URL doesn't already exist.
        """
        try:
            logger.debug(
                "Inserting data - URL: %s, Content (first 50 chars): %s, Embedding (first 5 dims): %s",
                url, content[:50], embedding[:5]
            )
            # Convert list to PostgreSQL-compatible array with proper formatting
            embedding_str = f"[{', '.join(map(str, embedding))}]"

            insert_query = """
            INSERT INTO scraptable (url, embedding, content)
            VALUES (%s, %s::vector, %s)
            ON CONFLICT (url) DO NOTHING;
            """
            self.cursor.execute(insert_query, (url, embedding_str, content))
            self.conn.commit()
            logger.info("Data inserted successfully for URL: %s", url)
        except Exception as e:
            logger.error("Failed to insert vector for URL %s: %s", url, e)
            self.conn.rollback()
            raise

    def query_similar(self, embedding: list, top_k: int = 5):
        """
        Queries the database for the most similar vectors based on the provided embedding.
        """
        try:
            logger.debug("Executing similarity query with top_k: %d", top_k)
            # Convert list to PostgreSQL-compatible array with proper formatting
            embedding_str = f"[{', '.join(map(str, embedding))}]"

            query = """
            SELECT id, url, content, 1 - (embedding <=> %s::vector) AS similarity
            FROM scraptable
            ORDER BY similarity DESC
            LIMIT %s;
            """
            self.cursor.execute(query, (embedding_str, top_k))
            results = self.cursor.fetchall()
            logger.info("Retrieved %d similar records.", len(results))
            return results
        except Exception as e:
            logger.error("Failed to query similar vectors: %s", e)
            raise

    def get_content_snippet(self, record_id: int):
        """
        Fetches a content snippet for a given record ID.
        """
        try:
            logger.debug("Fetching content snippet for record ID: %d", record_id)
            query = """
            SELECT content
            FROM scraptable
            WHERE id = %s;
            """
            self.cursor.execute(query, (record_id,))
            result = self.cursor.fetchone()

            if result and "content" in result:
                snippet = result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"]
                logger.debug("Snippet retrieved for record ID %d: %s", record_id, snippet)
                return snippet
            else:
                logger.warning("No content found for record ID: %d", record_id)
                return "Snippet unavailable."
        except Exception as e:
            logger.error("Failed to fetch snippet for record ID %d: %s", record_id, e)
            raise

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logger.info("Database connection closed.")