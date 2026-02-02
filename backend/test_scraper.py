"""Test script to verify RSS scraper functionality."""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import asyncio
import logging
from scrapers import RSScraper, RSS_SOURCES


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_scraper():
    """Test scraping all configured RSS sources."""
    print("\n" + "="*80)
    print("🌾 AGROMATE - RSS Scraper Test")
    print("="*80 + "\n")
    
    total_articles = 0
    
    for source in RSS_SOURCES:
        if not source["enabled"]:
            print(f"⏭️  Skipping {source['name']} (disabled)")
            continue
        
        print(f"\n📰 Testing: {source['name']}")
        print(f"   URL: {source['url']}")
        print("-" * 80)
        
        try:
            scraper = RSScraper(source_name=source["name"])
            news_items = await scraper.scrape(source["url"])
            
            print(f"✅ Success! Found {len(news_items)} articles\n")
            
            # Display first 3 articles as sample
            for i, news in enumerate(news_items[:3], 1):
                print(f"   [{i}] {news.title[:70]}...")
                print(f"       📅 {news.published_at or 'No date'}")
                print(f"       🔗 {news.url}")
                print()
            
            if len(news_items) > 3:
                print(f"   ... and {len(news_items) - 3} more articles\n")
            
            total_articles += len(news_items)
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
            continue
    
    print("="*80)
    print(f"🎯 Total articles scraped: {total_articles}")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(test_scraper())
