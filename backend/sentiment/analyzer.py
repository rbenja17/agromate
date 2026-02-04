"""Sentiment analyzer for agricultural news articles."""

import logging
from typing import List, Dict
from dataclasses import asdict

from models.news import News
from .llm_client import MockLLMClient

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Analyzes sentiment of agricultural news articles.
    
    Uses an LLM client (mock or real) to classify news as ALCISTA, BAJISTA, or NEUTRAL
    in relation to commodity prices (e.g., Soja/Soybean).
    """
    
    def __init__(self, llm_client: MockLLMClient = None):
        """
        Initialize the sentiment analyzer.
        
        Args:
            llm_client: LLM client instance (defaults to MockLLMClient if not provided)
        """
        self.llm_client = llm_client or MockLLMClient()
        logger.info(f"SentimentAnalyzer initialized with {type(self.llm_client).__name__}")
    
    def analyze_news(self, news_items: List[News]) -> List[Dict]:
        """
        Analyze sentiment for a list of news articles.
        
        Args:
            news_items: List of News objects to analyze
            
        Returns:
            List of dictionaries containing original news data plus sentiment analysis
        """
        enriched_news = []
        
        logger.info(f"Starting sentiment analysis for {len(news_items)} articles")
        
        for i, news in enumerate(news_items, 1):
            try:
                # Analyze the news title
                analysis = self.llm_client.analyze(news.title)
                
                # Rule: Filter out IRRELEVANT news
                if analysis.get("commodity") == "IRRELEVANT":
                    logger.info(f"Skipping irrelevant news: {news.title[:50]}...")
                    continue

                # Create enriched news item with sentiment data
                enriched_item = {
                    # Original news data
                    "title": news.title,
                    "source": news.source,
                    "url": news.url,
                    "published_at": news.published_at,
                    # Sentiment analysis results
                    "sentiment": analysis["sentiment"],
                    "confidence": analysis["confidence"],
                    "commodity": analysis.get("commodity", "GENERAL")
                }
                
                enriched_news.append(enriched_item)
                
                logger.debug(
                    f"[{i}/{len(news_items)}] {news.source}: "
                    f"{analysis['sentiment']} ({analysis['confidence']})"
                )
                
            except Exception as e:
                logger.error(f"Failed to analyze news '{news.title}': {e}")
                # Skip items that failed to analyze to avoid "Desconocido" in UI
                continue
        
        logger.info(f"Sentiment analysis completed: {len(enriched_news)} articles processed")
        
        return enriched_news
    
    def analyze_single(self, news: News) -> Dict:
        """
        Analyze sentiment for a single news article.
        
        Args:
            news: News object to analyze
            
        Returns:
            Dictionary containing news data plus sentiment analysis
        """
        results = self.analyze_news([news])
        return results[0] if results else None
    
    def get_sentiment_summary(self, enriched_news: List[Dict]) -> Dict:
        """
        Get aggregated sentiment statistics.
        
        Args:
            enriched_news: List of enriched news items from analyze_news()
            
        Returns:
            Dictionary with sentiment counts and percentages
        """
        total = len(enriched_news)
        if total == 0:
            return {"total": 0}
        
        alcista_count = sum(1 for item in enriched_news if item.get("sentiment") == "ALCISTA")
        bajista_count = sum(1 for item in enriched_news if item.get("sentiment") == "BAJISTA")
        neutral_count = sum(1 for item in enriched_news if item.get("sentiment") == "NEUTRAL")
        error_count = sum(1 for item in enriched_news if item.get("sentiment") == "ERROR")
        
        return {
            "total": total,
            "alcista": {
                "count": alcista_count,
                "percentage": round((alcista_count / total) * 100, 1)
            },
            "bajista": {
                "count": bajista_count,
                "percentage": round((bajista_count / total) * 100, 1)
            },
            "neutral": {
                "count": neutral_count,
                "percentage": round((neutral_count / total) * 100, 1)
            },
            "errors": error_count
        }
