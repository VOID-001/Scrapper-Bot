import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Application Configurations
APP_NAME = "Scrapper Bot"
VERSION = "1.0.0"

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector Database Configuration (PGVector)
PGVECTOR_HOST = os.getenv("PGVECTOR_HOST", "localhost")
PGVECTOR_PORT = int(os.getenv("PGVECTOR_PORT", 5432))
PGVECTOR_DB = os.getenv("PGVECTOR_DB", "vector_db")
PGVECTOR_USER = os.getenv("PGVECTOR_USER", "user")
PGVECTOR_PASSWORD = os.getenv("PGVECTOR_PASSWORD", "password")

# Web Scraping Settings
SCRAPER_USER_AGENT = os.getenv("SCRAPER_USER_AGENT", "ScrapperBot/1.0")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Other Constants
CHUNK_SIZE = 500  # Size of text chunks for embedding

# Validate Required Configurations
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables. Please configure it in a .env file.")