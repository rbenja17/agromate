"""Complete pipeline: Scraping → Sentiment Analysis → Database Storage."""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import asyncio
import logging
from typing import Dict

from scrapers import RSScraper, RSS_SOURCES
from sentiment import SentimentAnalyzer, MockLLMClient
from database import get_supabase_client, NewsRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def run_complete_pipeline():
    """Execute the complete Agromate pipeline."""
    print("\n" + "="*80)
    print("🌾 AGROMATE - Complete Pipeline Test")
    print("="*80 + "\n")
    
    print("Pipeline: RSS Scraping → Sentiment Analysis → Database Storage\n")
    print("-" * 80 + "\n")
    
    # Step 1: Scrape news from all sources
    print("📰 Step 1: Scraping news from all sources...\n")
    
    all_news = []
    for source in RSS_SOURCES:
        if not source["enabled"]:
            continue
        
        try:
            scraper = RSScraper(source_name=source["name"])
            news_items = await scraper.scrape(source["url"])
            
            # Limit to 3 articles per source for testing
            news_items = news_items[:3]
            all_news.extend(news_items)
            
            print(f"   ✅ {source['name']}: {len(news_items)} articles")
            
        except Exception as e:
            print(f"   ❌ {source['name']}: Failed ({e})")
    
    print(f"\n📊 Total scraped: {len(all_news)} articles\n")
    print("-" * 80 + "\n")
    
    # Step 2: Analyze sentiment
    print("🤖 Step 2: Analyzing sentiment...\n")
    
    analyzer = SentimentAnalyzer(llm_client=MockLLMClient(simulate_latency=False))
    enriched_news = analyzer.analyze_news(all_news)
    
    # Get summary
    summary = analyzer.get_sentiment_summary(enriched_news)
    
    print(f"✅ Analyzed {summary['total']} articles:\n")
    print(f"   🟢 ALCISTA:  {summary['alcista']['count']:2d} ({summary['alcista']['percentage']:5.1f}%)")
    print(f"   🔴 BAJISTA:  {summary['bajista']['count']:2d} ({summary['bajista']['percentage']:5.1f}%)")
    print(f"   ⚪ NEUTRAL:  {summary['neutral']['count']:2d} ({summary['neutral']['percentage']:5.1f}%)")
    print()
    
    print("-" * 80 + "\n")
    
    # Step 3: Save to database
    print("💾 Step 3: Saving to Supabase...\n")
    
    try:
        # Connect to Supabase
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Prepare sentiment data
        sentiment_data = {
            item["url"]: {
                "sentiment": item["sentiment"],
                "confidence": item["confidence"]
            }
            for item in enriched_news
        }
        
        # Upsert news
        results = repo.upsert_news(all_news, sentiment_data)
        
        print(f"✅ Saved {len(results)} articles to database\n")
        
    except Exception as e:
        print(f"❌ Database error: {e}\n")
        return
    
    print("-" * 80 + "\n")
    
    # Step 4: Verify data in database
    print("🔍 Step 4: Verifying database contents...\n")
    
    try:
        # Get recent news
        recent = repo.get_recent(hours=24, limit=5)
        
        print(f"Recent articles in database (showing 5):\n")
        for i, article in enumerate(recent[:5], 1):
            sentiment_emoji = {
                "ALCISTA": "🟢",
                "BAJISTA": "🔴",
                "NEUTRAL": "⚪"
            }.get(article.get("sentiment"), "❓")
            
            print(f"   [{i}] {article['title'][:60]}...")
            print(f"       {sentiment_emoji} {article.get('sentiment', 'N/A')} "
                  f"(conf: {article.get('confidence', 'N/A')})")
            print(f"       Source: {article['source']}")
            print()
        
        # Get overall stats
        stats = repo.count_by_sentiment()
        total_in_db = sum(stats.values())
        
        print(f"📈 Total articles in database: {total_in_db}\n")
        print("Sentiment distribution:")
        print(f"   🟢 ALCISTA:  {stats.get('ALCISTA', 0):3d}")
        print(f"   🔴 BAJISTA:  {stats.get('BAJISTA', 0):3d}")
        print(f"   ⚪ NEUTRAL:  {stats.get('NEUTRAL', 0):3d}")
        print(f"   ❓ NULL:     {stats.get('NULL', 0):3d}")
        print()
        
    except Exception as e:
        print(f"❌ Verification error: {e}\n")
    
    print("="*80)
    print("✅ Complete pipeline executed successfully!")
    print("="*80 + "\n")
    
    print("🎯 Summary:")
    print(f"   • Scraped:  {len(all_news)} articles")
    print(f"   • Analyzed: {len(enriched_news)} articles")
    print(f"   • Saved:    {len(results)} articles")
    print(f"   • Database: {total_in_db} total articles\n")


if __name__ == "__main__":
    asyncio.run(run_complete_pipeline())
