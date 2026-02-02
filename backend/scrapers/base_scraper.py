"""Abstract base class for news scrapers."""

from abc import ABC, abstractmethod
from typing import List
import logging

from models.news import News


logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class defining the interface for news scrapers.
    
    All concrete scraper implementations must inherit from this class
    and implement the scrape() method.
    """
    
    def __init__(self, source_name: str):
        """
        Initialize the scraper.
        
        Args:
            source_name: Human-readable name of the news source
        """
        self.source_name = source_name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def scrape(self, url: str) -> List[News]:
        """
        Scrape news from the given URL.
        
        Args:
            url: The RSS feed or webpage URL to scrape
            
        Returns:
            List of News objects parsed from the source
            
        Raises:
            Exception: If scraping fails (implementation-specific)
        """
        pass
    
    def _log_scrape_result(self, url: str, count: int) -> None:
        """
        Log the result of a scrape operation.
        
        Args:
            url: The URL that was scraped
            count: Number of articles scraped
        """
        self.logger.info(
            f"Scraped {count} articles from {self.source_name} ({url})"
        )
