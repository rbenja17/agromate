"""News model for scraped agricultural news articles."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class News:
    """
    Represents a scraped news article from agricultural RSS feeds.
    
    Attributes:
        title: The headline/title of the news article
        source: Name of the news source (e.g., 'Bichos de Campo')
        url: Full URL to the original article
        published_at: Publication timestamp (nullable if not provided by feed)
    """
    
    title: str
    source: str
    url: str
    published_at: Optional[datetime] = None
