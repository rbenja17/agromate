"""
Quick debug script to test daily trends endpoint.
"""
import sys
sys.path.insert(0, '.')

from database import get_supabase_client, NewsRepository
from datetime import datetime, timedelta

def test_daily_trends():
    client = get_supabase_client()
    repo = NewsRepository(client)
    
    # Get some news
    all_news = repo.get_all(limit=5)
    
    print(f"Found {len(all_news)} news items")
    
    for news in all_news[:2]:
        print(f"\nNews ID: {news.get('id')}")
        print(f"Published at: {news.get('published_at')}")
        print(f"Type: {type(news.get('published_at'))}")
        
        # Try to parse
        if news.get('published_at'):
            try:
                pub_date = datetime.fromisoformat(news['published_at'].replace('Z', '+00:00'))
                print(f"Parsed successfully: {pub_date}")
            except Exception as e:
                print(f"ERROR parsing: {e}")

if __name__ == "__main__":
    test_daily_trends()
