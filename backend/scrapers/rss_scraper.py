"""RSS feed scraper implementation using feedparser."""

from datetime import datetime
from typing import List, Optional
import feedparser
from email.utils import parsedate_to_datetime
import logging

from models.news import News
from .base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class RSScraper(BaseScraper):
    """
    Scraper for RSS feeds using the feedparser library.
    
    Handles various RSS/Atom feed formats and normalizes date parsing.
    """
    
    def __init__(self, source_name: str, timeout: int = 10):
        """
        Initialize RSS scraper.
        
        Args:
            source_name: Human-readable name of the news source
            timeout: Request timeout in seconds (default: 10)
        """
        super().__init__(source_name)
        self.timeout = timeout
    
    async def scrape(self, url: str) -> List[News]:
        """
        Scrape news articles from an RSS feed.
        
        Args:
            url: RSS feed URL to scrape
            
        Returns:
            List of validated News objects
            
        Raises:
            ValueError: If feed cannot be parsed or is empty
            ConnectionError: If feed cannot be reached
        """
        try:
            self.logger.info(f"Fetching RSS feed from {url}")
            
            # Parse the RSS feed
            feed = feedparser.parse(url)
            
            # Check for feed errors
            if feed.bozo and not feed.entries:
                error_msg = getattr(feed, 'bozo_exception', 'Unknown error')
                raise ValueError(f"Failed to parse RSS feed: {error_msg}")
            
            # Check if feed has entries
            if not feed.entries:
                self.logger.warning(f"No entries found in feed: {url}")
                return []
            
            # Parse each entry into News objects
            news_items: List[News] = []
            for entry in feed.entries:
                try:
                    news_item = self._parse_entry(entry)
                    if news_item:
                        news_items.append(news_item)
                except Exception as e:
                    self.logger.error(
                        f"Failed to parse entry '{getattr(entry, 'title', 'Unknown')}': {e}"
                    )
                    continue
            
            self._log_scrape_result(url, len(news_items))
            return news_items
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            raise
    
    def _parse_entry(self, entry) -> Optional[News]:
        """
        Parse a single RSS feed entry into a News object.
        
        Args:
            entry: feedparser entry object
            
        Returns:
            Validated News object or None if parsing fails
        """
        # Extract title
        title = getattr(entry, 'title', None)
        if not title:
            self.logger.debug("Skipping entry without title")
            return None
        
        # Extract URL (try multiple possible fields)
        url = getattr(entry, 'link', None) or getattr(entry, 'id', None)
        if not url:
            self.logger.debug(f"Skipping entry '{title}': no URL found")
            return None
        
        # Parse publication date
        published_at = self._parse_date(entry)
        
        # Create and validate News object
        try:
            news = News(
                title=title.strip(),
                source=self.source_name,
                url=url,
                published_at=published_at
            )
            return news
        except Exception as e:
            self.logger.error(f"Validation failed for entry '{title}': {e}")
            return None
    
    def _parse_date(self, entry) -> Optional[datetime]:
        """
        Extract and normalize publication date from RSS entry.
        
        Tries multiple common RSS date fields and formats.
        
        Args:
            entry: feedparser entry object
            
        Returns:
            Normalized datetime object (UTC) or None if date cannot be parsed
        """
        # Try different possible date fields in order of preference
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        
        for field in date_fields:
            time_struct = getattr(entry, field, None)
            if time_struct:
                try:
                    # Convert time.struct_time to datetime
                    return datetime(*time_struct[:6])
                except Exception as e:
                    self.logger.debug(f"Failed to parse {field}: {e}")
                    continue
        
        # Try parsing string dates as fallback
        string_fields = ['published', 'updated', 'created']
        for field in string_fields:
            date_string = getattr(entry, field, None)
            if date_string:
                try:
                    # Use email.utils for RFC 2822 date parsing
                    return parsedate_to_datetime(date_string)
                except Exception as e:
                    self.logger.debug(f"Failed to parse {field} string: {e}")
                    continue
        
        self.logger.debug("No valid date found in entry")
        return None
