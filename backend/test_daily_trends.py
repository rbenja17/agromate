"""
Test daily trends endpoint directly.
"""
import sys
sys.path.insert(0, '.')

from database import get_supabase_client, NewsRepository
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_daily_endpoint():
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        days = 7
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        print(f"Date range: {start_date} to {end_date}")
        
        # Fetch all news in range
        all_news = repo.get_all(limit=1000)
        print(f"Total news: {len(all_news)}")
        
        # Filter by date and group by day
        daily_data = {}
        
        for news in all_news:
            if not news.get('published_at'):
                print(f"Skipping news without date: {news.get('id')}")
                continue
                
            try:
                pub_date = datetime.fromisoformat(news['published_at'].replace('Z', '+00:00'))
            except Exception as e:
                print(f"Error parsing date for {news.get('id')}: {e}")
                print(f"Date value: {news['published_at']}")
                continue
            
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
            
            sentiment = news.get('sentiment', 'NEUTRAL').upper()
            if sentiment == 'ALCISTA':
                daily_data[date_key]['alcista'] += 1
            elif sentiment == 'BAJISTA':
                daily_data[date_key]['bajista'] += 1
            else:
                daily_data[date_key]['neutral'] += 1
        
        # Convert to sorted list
        result = sorted(daily_data.values(), key=lambda x: x['date'])
        
        print(f"\nResult:")
        for day in result:
            print(f"  {day}")
        
        return {
            "period": f"{days}d",
            "data": result
        }
        
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise

if __name__ == "__main__":
    test_daily_endpoint()
