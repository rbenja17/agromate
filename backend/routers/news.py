"""News API endpoints."""

import asyncio
import logging
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse

from database import get_supabase_client, NewsRepository
from schemas import NewsResponse, NewsListResponse, SentimentStats, PipelineResponse
from scrapers import RSScraper, RSS_SOURCES
from sentiment import SentimentAnalyzer, MockLLMClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["news"])


def dict_to_news_response(news_dict: dict) -> NewsResponse:
    """
    Convert a news dictionary from database to NewsResponse schema.
    
    Args:
        news_dict: News record from database
        
    Returns:
        NewsResponse Pydantic model
    """
    return NewsResponse(
        id=news_dict["id"],
        title=news_dict["title"],
        source=news_dict["source"],
        url=news_dict["url"],
        published_at=news_dict.get("published_at"),
        sentiment=news_dict.get("sentiment"),
        confidence=news_dict.get("confidence"),
        commodity=news_dict.get("commodity", "SOJA"),
        created_at=news_dict["created_at"],
        updated_at=news_dict["updated_at"]
    )


@router.get("/news", response_model=NewsListResponse)
async def get_news(
    limit: int = Query(default=50, ge=1, le=200, description="Maximum number of articles to return"),
    sentiment: Optional[str] = Query(default=None, description="Filter by sentiment (ALCISTA/BAJISTA/NEUTRAL)"),
    source: Optional[List[str]] = Query(default=None, description="Filter by source names (multi-select)"),  # Cambiado a List[str]
    commodity: Optional[str] = Query(default=None, description="Filter by commodity (SOJA/MAÍZ/TRIGO/GIRASOL/CEBADA/SORGO/GENERAL)"),
    date_from: Optional[str] = Query(default=None, description="Filter from date (ISO format: YYYY-MM-DD)"),
    date_to: Optional[str] = Query(default=None, description="Filter to date (ISO format: YYYY-MM-DD)")
):
    """
    Get a list of news articles with optional filters.
    
    Parameters:
        - **limit**: Maximum number of articles (default: 50, max: 200)
        - **sentiment**: Optional filter by sentiment type (ALCISTA/BAJISTA/NEUTRAL)
        - **source**: Optional filter by source names (can be specified multiple times for multi-select)
        - **commodity**: Optional filter by commodity (SOJA/MAÍZ/TRIGO/GIRASOL/CEBADA/SORGO/GENERAL)
        - **date_from**: Optional start date filter (YYYY-MM-DD)
        - **date_to**: Optional end date filter (YYYY-MM-DD)
        
    Returns:
        List of news articles with sentiment analysis
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Check if any filter is applied
        has_filters = any([sentiment, source, commodity, date_from, date_to])
        
        if has_filters:
            news_list = repo.get_filtered(
                source=source,  # Ahora acepta List[str]
                sentiment=sentiment,
                commodity=commodity,
                date_from=date_from,
                date_to=date_to,
                limit=limit
            )
        else:
            news_list = repo.get_all(limit=limit)
        
        # Convert to NewsResponse schema
        articles = [dict_to_news_response(news) for news in news_list]
        
        return NewsListResponse(
            total=len(articles),
            articles=articles
        )
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


@router.get("/news/{news_id}", response_model=NewsResponse)
async def get_news_by_id(news_id: str):
    """
    Get a single news article by ID.
    
    Parameters:
        - **news_id**: UUID of the news article
        
    Returns:
        Single news article with sentiment analysis
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        news = repo.get_by_id(news_id)
        
        if not news:
            raise HTTPException(status_code=404, detail=f"News article {news_id} not found")
        
        return dict_to_news_response(news)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news {news_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


@router.get("/stats", response_model=SentimentStats)
async def get_sentiment_stats():
    """
    Get sentiment statistics across all news articles.
    
    Returns:
        Aggregate statistics of sentiment distribution
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Get counts
        counts = repo.count_by_sentiment()
        
        total = sum(counts.values())
        alcista = counts.get("ALCISTA", 0)
        bajista = counts.get("BAJISTA", 0)
        neutral = counts.get("NEUTRAL", 0)
        null = counts.get("NULL", 0)
        
        # Calculate percentages
        alcista_pct = (alcista / total * 100) if total > 0 else 0.0
        bajista_pct = (bajista / total * 100) if total > 0 else 0.0
        neutral_pct = (neutral / total * 100) if total > 0 else 0.0
        
        return SentimentStats(
            total=total,
            alcista=alcista,
            bajista=bajista,
            neutral=neutral,
            null=null,
            alcista_percentage=round(alcista_pct, 1),
            bajista_percentage=round(bajista_pct, 1),
            neutral_percentage=round(neutral_pct, 1)
        )
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


async def run_pipeline_task():
    """Background task to run the complete pipeline."""
    logger.info("Starting pipeline task in background...")
    
    try:
        # Step 1: Scrape news
        all_news = []
        for source in RSS_SOURCES:
            if not source["enabled"]:
                continue
            
            try:
                scraper = RSScraper(source_name=source["name"])
                news_items = await scraper.scrape(source["url"])
                
                # Limit to avoid overload
                news_items = news_items[:10]
                all_news.extend(news_items)
                
                logger.info(f"Scraped {len(news_items)} from {source['name']}")
                
            except Exception as e:
                logger.error(f"Failed to scrape {source['name']}: {e}")
        
        logger.info(f"Total scraped: {len(all_news)} articles")
        
        # Step 2: Analyze sentiment with GROQ (real LLM)
        from sentiment.llm_client import get_llm_client
        llm_client = get_llm_client(use_mock=False)  # Use real Groq API
        analyzer = SentimentAnalyzer(llm_client=llm_client)
        enriched_news = analyzer.analyze_news(all_news)
        
        logger.info(f"Analyzed {len(enriched_news)} articles")
        
        # Step 3: Save to database
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Filter out items without valid sentiment before saving
        valid_enriched_news = [item for item in enriched_news if item.get("sentiment")]
        
        sentiment_data = {
            item["url"]: {
                "sentiment": item["sentiment"],
                "confidence": item["confidence"]
            }
            for item in valid_enriched_news
        }
        
        # Only upsert news that have been successfully enriched
        # We extract the original news items corresponding to the enriched ones
        valid_urls = set(item["url"] for item in valid_enriched_news)
        valid_news_objects = [n for n in all_news if str(n.url) in valid_urls]
        
        if valid_news_objects:
             results = repo.upsert_news(valid_news_objects, sentiment_data)
             logger.info(f"Pipeline completed: {len(results)} articles saved")
        else:
             logger.info("Pipeline completed: No valid articles to save")
        
    except Exception as e:
        logger.error(f"Pipeline task failed: {e}")


@router.post("/pipeline/run", response_model=PipelineResponse)
async def run_pipeline(background_tasks: BackgroundTasks):
    """
    Trigger the complete pipeline (Scraping → Analysis → Storage) in background.
    
    This endpoint starts the pipeline asynchronously and returns immediately.
    The pipeline runs in the background without blocking the API.
    
    Returns:
        Status message indicating pipeline has started
    """
    try:
        # Add pipeline task to background
        background_tasks.add_task(run_pipeline_task)
        
        return PipelineResponse(
            status="running",
            message="Pipeline started in background. Check /api/stats for updates."
        )
        
    except Exception as e:
        logger.error(f"Error starting pipeline: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start pipeline: {str(e)}")


@router.get("/recent", response_model=NewsListResponse)
async def get_recent_news(
    hours: int = Query(default=24, ge=1, le=168, description="Number of hours to look back")
):
    """
    Get recent news articles from the last N hours.
    
    Parameters:
        - **hours**: Number of hours to look back (default: 24, max: 168/7 days)
        
    Returns:
        List of recent news articles
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        news_list = repo.get_recent(hours=hours, limit=100)
        
        # Convert to NewsResponse schema
        articles = [dict_to_news_response(news) for news in news_list]
        
        return NewsListResponse(
            total=len(articles),
            articles=articles
        )
        
    except Exception as e:
        logger.error(f"Error fetching recent news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch recent news: {str(e)}")


@router.get("/sources")
async def get_available_sources():
    """
    Get list of available news sources.
    
    Returns:
        List of unique source names
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        all_news = repo.get_all(limit=1000)
        sources = list(set(news.get('source', 'Unknown') for news in all_news))
        sources.sort()
        
        return {"sources": sources}
        
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))
