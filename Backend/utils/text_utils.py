import re
from typing import List

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing excessive whitespace, special characters, and non-alphanumeric content.

    Args:
        text (str): The raw text to clean.

    Returns:
        str: The cleaned text.
    """
    # Remove non-alphanumeric characters (except spaces)
    text = re.sub(r"[^\w\s]", "", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Strip leading and trailing whitespace
    return text.strip()

def chunk_text(text: str, chunk_size: int) -> List[str]:
    """
    Splits the input text into smaller chunks of a specified size.
    """
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]