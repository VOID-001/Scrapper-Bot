from openai import OpenAI
from typing import List
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def embed_text(texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """
    Generates embeddings for a list of texts using OpenAI's embedding model.
    """
    try:
        # Call OpenAI API to generate embeddings
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings: {e}")