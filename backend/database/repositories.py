"""Data repositories for database operations."""

import logging
from typing import List, Optional, Dict
from datetime import datetime
from supabase import Client

from models.news import News

logger = logging.getLogger(__name__)


class NewsRepository:
    """
    Repository for news articles CRUD operations with Supabase.
    """
    
    def __init__(self, client: Client):
        """
        Initialize the news repository.
        
        Args:
            client: Configured Supabase client
        """
        self.client = client
        self.table_name = "news"
    
    def create(self, news: News, sentiment: str = None, confidence: float = None) -> Dict:
        """
        Create a new news article in the database.
        
        Args:
            news: News object to save
            sentiment: Optional sentiment classification (ALCISTA/BAJISTA/NEUTRAL)
            confidence: Optional confidence score (0.0-1.0)
            
        Returns:
            Created news record as dict
            
        Raises:
            Exception: If creation fails (e.g., duplicate URL)
        """
        try:
            data = {
                "title": news.title,
                "source": news.source,
                "url": str(news.url),
                "published_at": news.published_at.isoformat() if news.published_at else None,
                "sentiment": sentiment,
                "confidence": confidence
            }
            
            response = self.client.table(self.table_name).insert(data).execute()
            
            logger.info(f"Created news: {news.title[:50]}...")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Failed to create news '{news.title}': {e}")
            raise
    
    def create_batch(self, enriched_news: List[Dict]) -> List[Dict]:
        """
        Create multiple news articles in batch.
        
        Args:
            enriched_news: List of dicts with news data + sentiment
            
        Returns:
            List of created records
        """
        try:
            # Prepare data for insertion
            data_list = []
            for item in enriched_news:
                data = {
                    "title": item["title"],
                    "source": item["source"],
                    "url": item["url"],
                    "published_at": item["published_at"].isoformat() if item.get("published_at") else None,
                    "sentiment": item.get("sentiment"),
                    "confidence": item.get("confidence"),
                    "commodity": item.get("commodity", "GENERAL")  # NUEVO
                }
                data_list.append(data)
            
            # Insert batch
            response = self.client.table(self.table_name).insert(data_list).execute()
            
            logger.info(f"Created {len(data_list)} news articles in batch")
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to create batch: {e}")
            raise
    
    def upsert_news(self, news_list: List[News], sentiment_data: Dict[str, Dict] = None) -> List[Dict]:
        """
        Upsert (insert or update) news articles, avoiding duplicates by URL.
        
        This method will insert new articles or update existing ones based on URL.
        Perfect for scraping operations where the same article might be scraped multiple times.
        
        Args:
            news_list: List of News dataclass objects to upsert
            sentiment_data: Optional dict mapping URLs to sentiment/confidence data
                           Format: {url: {"sentiment": "ALCISTA", "confidence": 0.92}}
            
        Returns:
            List of upserted records
            
        Example:
            news_list = [News(...), News(...)]
            sentiment_data = {
                "https://example.com/news1": {"sentiment": "ALCISTA", "confidence": 0.9}
            }
            results = repo.upsert_news(news_list, sentiment_data)
        """
        try:
            from dataclasses import asdict
            
            # Convert News dataclass objects to dictionaries
            data_list = []
            for news in news_list:
                # Convert dataclass to dict
                news_dict = asdict(news)
                
                # Convert URL to string if it's not already
                news_dict["url"] = str(news_dict["url"])
                
                # Convert datetime to ISO string if present
                if news_dict.get("published_at"):
                    news_dict["published_at"] = news_dict["published_at"].isoformat()
                
                # Add sentiment data if provided
                if sentiment_data and news_dict["url"] in sentiment_data:
                    sentiment_info = sentiment_data[news_dict["url"]]
                    news_dict["sentiment"] = sentiment_info.get("sentiment")
                    news_dict["confidence"] = sentiment_info.get("confidence")
                
                data_list.append(news_dict)
            
            # Upsert with conflict resolution on URL
            response = self.client.table(self.table_name)\
                .upsert(data_list, on_conflict="url")\
                .execute()
            
            logger.info(f"Upserted {len(data_list)} news articles (duplicates updated)")
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to upsert news: {e}")
            raise
    
    def get_by_id(self, news_id: str) -> Optional[Dict]:
        """
        Get a news article by ID.
        
        Args:
            news_id: UUID of the news article
            
        Returns:
            News record as dict or None if not found
        """
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .eq("id", news_id)\
                .execute()
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Failed to get news by ID {news_id}: {e}")
            return None
    
    def get_by_url(self, url: str) -> Optional[Dict]:
        """
        Get a news article by URL (useful for checking duplicates).
        
        Args:
            url: Article URL
            
        Returns:
            News record as dict or None if not found
        """
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .eq("url", url)\
                .execute()
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Failed to get news by URL: {e}")
            return None
    
    def exists(self, url: str) -> bool:
        """
        Check if a news article already exists by URL.
        
        Args:
            url: Article URL to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.get_by_url(url) is not None
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get all news articles with pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of news records
        """
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .order("published_at", desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to get all news: {e}")
            return []
    
    def get_by_sentiment(self, sentiment: str, limit: int = 100) -> List[Dict]:
        """
        Get news articles by sentiment.
        
        Args:
            sentiment: Sentiment to filter (ALCISTA/BAJISTA/NEUTRAL)
            limit: Maximum number of records
            
        Returns:
            List of news records
        """
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .eq("sentiment", sentiment)\
                .order("published_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to get news by sentiment {sentiment}: {e}")
            return []
    
    def get_recent(self, hours: int = 24, limit: int = 100) -> List[Dict]:
        """
        Get recent news articles from the last N hours.
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of records
            
        Returns:
            List of recent news records
        """
        try:
            # Calculate timestamp
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            
            response = self.client.table(self.table_name)\
                .select("*")\
                .gte("published_at", cutoff.isoformat())\
                .order("published_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to get recent news: {e}")
            return []
    
    def get_filtered(
        self,
        source: List[str] = None,  # Cambiado de str a List[str]
        sentiment: str = None,
        commodity: str = None,
        date_from: str = None,
        date_to: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get news articles with multiple filters.
        
        Args:
            source: Filter by source names (list for multi-select, OR operation)
            sentiment: Filter by sentiment (ALCISTA/BAJISTA/NEUTRAL)
            commodity: Filter by commodity (SOJA/MAÍZ/TRIGO/GIRASOL/CEBADA/SORGO/GENERAL)
            date_from: Filter articles published after this date (ISO format)
            date_to: Filter articles published before this date (ISO format)
            limit: Maximum number of records
            
        Returns:
            List of filtered news records
        """
        try:
            query = (
                self.client
                .table(self.table_name)
                .select("*")
            )
            
            # Apply filters
            if source and len(source) > 0:
                # Multi-select: use .in_() for OR operation
                query = query.in_("source", source)
            
            if sentiment:
                query = query.eq("sentiment", sentiment.upper())
            
            if commodity:
                query = query.eq("commodity", commodity.upper())
            
            if date_from:
                query = query.gte("published_at", date_from)
            
            if date_to:
                query = query.lte("published_at", date_to)
            
            # Order and limit
            result = (
                query
                .order("published_at", desc=True)
                .limit(limit)
                .execute()
            )
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting filtered news: {e}")
            return []
    
    def update_sentiment(self, news_id: str, sentiment: str, confidence: float) -> Dict:
        """
        Update sentiment analysis for a news article.
        
        Args:
            news_id: UUID of the news article
            sentiment: Sentiment classification
            confidence: Confidence score
            
        Returns:
            Updated news record
        """
        try:
            response = self.client.table(self.table_name)\
                .update({"sentiment": sentiment, "confidence": confidence})\
                .eq("id", news_id)\
                .execute()
            
            logger.info(f"Updated sentiment for news {news_id}: {sentiment} ({confidence})")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Failed to update sentiment for {news_id}: {e}")
            raise
    
    def delete(self, news_id: str) -> bool:
        """
        Delete a news article.
        
        Args:
            news_id: UUID of the news article
            
        Returns:
            True if deleted successfully
        """
        try:
            self.client.table(self.table_name)\
                .delete()\
                .eq("id", news_id)\
                .execute()
            
            logger.info(f"Deleted news {news_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete news {news_id}: {e}")
            return False
    
    def count_by_sentiment(self) -> Dict[str, int]:
        """
        Get count of articles by sentiment.
        
        Returns:
            Dictionary with sentiment counts
        """
        try:
            # Get all sentiments
            response = self.client.table(self.table_name)\
                .select("sentiment")\
                .execute()
            
            # Count sentiments
            counts = {"ALCISTA": 0, "BAJISTA": 0, "NEUTRAL": 0, "NULL": 0}
            for record in response.data:
                sentiment = record.get("sentiment") or "NULL"
                if sentiment in counts:
                    counts[sentiment] += 1
            
            return counts
            
        except Exception as e:
            logger.error(f"Failed to count by sentiment: {e}")
            return {}
