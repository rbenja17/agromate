"""
Trends router for historical sentiment data visualization.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

from database import get_supabase_client, NewsRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/trends", tags=["trends"])


def calculate_weighted_sentiment(items):
    """
    Calcula un score de sentimiento ponderado por la confianza.
    Retorna un valor entre -1 (Totalmente Bajista) y 1 (Totalmente Alcista).
    
    Args:
        items: Lista de noticias con 'sentiment' y 'confidence'
        
    Returns:
        float: Score ponderado entre -1 y 1
    """
    if not items:
        return 0.0
    
    # Filtramos por sentimiento
    alcista_items = [i for i in items if (i.get('sentiment') or '').upper() == 'ALCISTA']
    bajista_items = [i for i in items if (i.get('sentiment') or '').upper() == 'BAJISTA']
    
    # Sumamos la confianza (Confidence Mass)
    # Si no hay 'confidence', asumimos 0.5 por defecto
    weighted_alcista = sum(float(i.get('confidence', 0.5)) for i in alcista_items)
    weighted_bajista = sum(float(i.get('confidence', 0.5)) for i in bajista_items)
    
    total_weight = weighted_alcista + weighted_bajista
    
    if total_weight == 0:
        return 0.0
        
    # Fórmula: (Peso Alcista - Peso Bajista) / Peso Total
    return (weighted_alcista - weighted_bajista) / total_weight


@router.get("/daily")
async def get_daily_trends(
    days: int = Query(default=7, ge=1, le=30),
    source: Optional[str] = Query(default=None, description="Filter by source name"),
    sentiment: Optional[str] = Query(default=None, description="Filter by sentiment"),
    date_from: Optional[str] = Query(default=None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(default=None, description="Filter to date (ISO format)")
):
    """
    Get daily sentiment trends for the last N days.
    
    Returns count of ALCISTA, BAJISTA, NEUTRAL per day.
    Supports filtering by source, sentiment, and date range.
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Get date range (use UTC timezone to match DB timestamps)
        from datetime import timezone
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # Use filtered query if filters provided
        has_filters = source or sentiment or date_from or date_to
        if has_filters:
            all_news = repo.get_filtered(
                source=source,
                sentiment=sentiment,
                date_from=date_from,
                date_to=date_to,
                limit=1000
            )
        else:
            all_news = repo.get_all(limit=1000)
        
        # Filter by date and group by day
        daily_data = {}
        
        for news in all_news:
            if not news.get('published_at'):
                continue
                
            pub_date = datetime.fromisoformat(news['published_at'].replace('Z', '+00:00'))
            
            if pub_date < start_date:
                continue
                
            date_key = pub_date.strftime('%Y-%m-%d')
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "date": date_key,
                    "alcista": 0,
                    "bajista": 0,
                    "neutral": 0
                }
            
            news_sentiment = (news.get('sentiment') or 'NEUTRAL').upper()
            if news_sentiment == 'ALCISTA':
                daily_data[date_key]['alcista'] += 1
            elif news_sentiment == 'BAJISTA':
                daily_data[date_key]['bajista'] += 1
            else:
                daily_data[date_key]['neutral'] += 1
        
        # Convert to sorted list
        result = sorted(daily_data.values(), key=lambda x: x['date'])
        
        return {
            "period": f"{days}d",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error getting daily trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-source")
async def get_trends_by_source(
    source: Optional[str] = Query(default=None, description="Filter by source name"),
    sentiment: Optional[str] = Query(default=None, description="Filter by sentiment"),
    date_from: Optional[str] = Query(default=None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(default=None, description="Filter to date (ISO format)")
):
    """
    Get sentiment distribution by news source.
    
    Returns count of ALCISTA, BAJISTA, NEUTRAL per source.
    Supports filtering.
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Use filtered query if filters provided
        has_filters = source or sentiment or date_from or date_to
        if has_filters:
            all_news = repo.get_filtered(
                source=source,
                sentiment=sentiment,
                date_from=date_from,
                date_to=date_to,
                limit=1000
            )
        else:
            all_news = repo.get_all(limit=1000)
        
        source_data = {}
        
        for news in all_news:
            news_source = news.get('source', 'Unknown')
            
            if news_source not in source_data:
                source_data[news_source] = {
                    "source": news_source,
                    "alcista": 0,
                    "bajista": 0,
                    "neutral": 0,
                    "total": 0
                }
            
            news_sentiment = (news.get('sentiment') or 'NEUTRAL').upper()
            if news_sentiment == 'ALCISTA':
                source_data[news_source]['alcista'] += 1
            elif news_sentiment == 'BAJISTA':
                source_data[news_source]['bajista'] += 1
            else:
                source_data[news_source]['neutral'] += 1
            
            source_data[news_source]['total'] += 1
        
        return {
            "data": list(source_data.values())
        }
        
    except Exception as e:
        logger.error(f"Error getting source trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline")
async def get_sentiment_timeline(
    days: int = Query(default=7, ge=1, le=30),
    source: Optional[str] = Query(default=None, description="Filter by source name"),
    sentiment: Optional[str] = Query(default=None, description="Filter by sentiment"),
    date_from: Optional[str] = Query(default=None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(default=None, description="Filter to date (ISO format)")
):
    """
    Get sentiment score timeline with confidence weighting.
    
    Calculates a weighted sentiment score (-1 to +1) per day where:
    - +1 = all ALCISTA (weighted by confidence)
    - -1 = all BAJISTA (weighted by confidence)
    - 0 = balanced or all NEUTRAL
    
    News with higher confidence have more impact on the score.
    Supports filtering by source, sentiment, and date range.
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        from datetime import timezone
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # Use filtered query if filters provided
        has_filters = source or sentiment or date_from or date_to
        if has_filters:
            all_news = repo.get_filtered(
                source=source,
                sentiment=sentiment,
                date_from=date_from,
                date_to=date_to,
                limit=1000
            )
        else:
            all_news = repo.get_all(limit=1000)
        
        # Group news by date
        daily_news = {}
        
        for news in all_news:
            if not news.get('published_at'):
                continue
                
            pub_date = datetime.fromisoformat(news['published_at'].replace('Z', '+00:00'))
            
            if pub_date < start_date:
                continue
                
            date_key = pub_date.strftime('%Y-%m-%d')
            
            if date_key not in daily_news:
                daily_news[date_key] = []
            
            daily_news[date_key].append(news)
        
        # Calculate weighted scores for each day
        timeline = []
        for date_key, items in daily_news.items():
            score = calculate_weighted_sentiment(items)
            
            timeline.append({
                "date": date_key,
                "sentiment_score": round(score, 2)
            })
        
        timeline.sort(key=lambda x: x['date'])
        
        return {
            "period": f"{days}d",
            "data": timeline
        }
        
    except Exception as e:
        logger.error(f"Error getting timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))
