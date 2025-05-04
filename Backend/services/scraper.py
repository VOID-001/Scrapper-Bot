import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from services.rag import ingest_and_store
from services.vectorstore import VectorDB
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self, base_url, max_depth=1):

        self.base_url = base_url
        self.max_depth = max_depth
        self.visited_urls = set()
        self.db = VectorDB()

    def scrape(self):
        """
        Begins the scraping process starting from the base URL.
        """
        logger.info("Starting scrape for base URL: %s", self.base_url)
        self._crawl(self.base_url, 0)
        logger.info("All extracted data has been stored in pgvector > scraptable > embedding.")
        self.db.close()

    def _crawl(self, url, depth):
        """
        Recursively crawls the given URL up to the specified depth.

        Args:
            url (str): The URL to crawl.
            depth (int): The current depth of the crawl.
        """
        if depth > self.max_depth:
            logger.debug("Reached maximum depth at URL: %s", url)
            return
        if url in self.visited_urls:
            logger.debug("URL already visited: %s", url)
            return

        logger.info("Crawling URL: %s (depth: %d)", url, depth)
        self.visited_urls.add(url)

        try:
            # Step 1: Perform the HTTP request
            logger.debug("Sending GET request to URL: %s", url)
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Successfully fetched content from URL: %s", url)

            # Step 2: Parse the HTML content
            logger.debug("Parsing HTML content from URL: %s", url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = self._clean_text(soup.get_text())
            logger.debug("Cleaned content (first 100 characters): %s", content[:100])

            # Step 3: Store the scraped content with embeddings in the database
            logger.info("Storing scraped content in database for URL: %s", url)
            self._store_to_db(content, url)

            # Step 4: Find and crawl links on the page
            logger.debug("Extracting links from URL: %s", url)
            links = self._extract_links(soup, url)
            for link in links:
                self._crawl(link, depth + 1)

        except requests.exceptions.RequestException as e:
            logger.error("HTTP request failed for URL %s: %s", url, e)
        except Exception as e:
            logger.error("Unexpected error during scraping for URL %s: %s", url, e)

    def _extract_links(self, soup, base_url):
        """
        Extracts and normalizes links from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.
            base_url (str): The base URL to resolve relative links.

        Returns:
            list: A list of normalized URLs.
        """
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Normalize the link to an absolute URL
            full_url = urljoin(base_url, href)
            # Only include links within the same domain
            if full_url.startswith(self.base_url):
                links.append(full_url)
        logger.debug("Found %d links on the page: %s", len(links), base_url)
        return links

    def _clean_text(self, text):
        """
        Cleans the extracted text by removing extra whitespace, newlines, and non-alphanumeric characters.

        Args:
            text (str): The raw text to clean.

        Returns:
            str: The cleaned text.
        """
        logger.debug("Cleaning extracted text...")
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
        text = text.strip()
        logger.debug("Cleaned text (first 100 characters): %s", text[:100])
        return text

    def _store_to_db(self, content, url):
        """
        Generates embeddings for the content and stores them in the database.

        Args:
            content (str): The cleaned text content.
            url (str): The URL of the content.
        """
        try:
            # Call the ingestion pipeline to generate embeddings and store them
            ingest_and_store(content, url)
            logger.info("Content for URL %s successfully stored in the database.", url)
        except Exception as e:
            logger.error("Failed to store content for URL %s: %s", url, e)


if __name__ == "__main__":
    # Example usage
    BASE_URL = "https://www.scrapethissite.com/"
    MAX_DEPTH = 2

    scraper = Scraper(BASE_URL, MAX_DEPTH)
    scraper.scrape()