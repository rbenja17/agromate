"""Test script for database connection and operations."""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import asyncio
import logging
from datetime import datetime
from dataclasses import asdict

from models.news import News
from database import get_supabase_client, NewsRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_database_connection():
    """Test Supabase connection and basic CRUD operations."""
    print("\n" + "="*80)
    print("🗄️  AGROMATE - Database Connection Test")
    print("="*80 + "\n")
    
    # Step 1: Initialize Supabase client
    print("📡 Step 1: Connecting to Supabase...\n")
    
    try:
        client = get_supabase_client()
        print("✅ Successfully connected to Supabase!")
        print(f"   URL: {client.supabase_url}\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}\n")
        return
    
    print("-" * 80 + "\n")
    
    # Step 2: Initialize repository
    print("📦 Step 2: Initializing NewsRepository...\n")
    repo = NewsRepository(client)
    print("✅ Repository initialized\n")
    
    print("-" * 80 + "\n")
    
    # Step 3: Create test news
    print("📰 Step 3: Creating test news articles...\n")
    
    test_news = [
        News(
            title="Test: Soja alcanza precios récord en Chicago",
            source="Test Source",
            url="https://test.agromate.com/soja-record-1",
            published_at=datetime.now()
        ),
        News(
            title="Test: Sequía afecta cultivos de maíz en Argentina",
            source="Test Source",
            url="https://test.agromate.com/sequia-maiz-2",
            published_at=datetime.now()
        ),
        News(
            title="Test: Exportaciones de trigo superan expectativas",
            source="Test Source",
            url="https://test.agromate.com/trigo-export-3",
            published_at=datetime.now()
        )
    ]
    
    for i, news in enumerate(test_news, 1):
        print(f"   [{i}] {news.title}")
        print(f"       URL: {news.url}")
    
    print()
    print("-" * 80 + "\n")
    
    # Step 4: Upsert news (with simulated sentiment)
    print("💾 Step 4: Upserting news to database...\n")
    
    # Simulate sentiment data
    sentiment_data = {
        "https://test.agromate.com/soja-record-1": {
            "sentiment": "ALCISTA",
            "confidence": 0.95
        },
        "https://test.agromate.com/sequia-maiz-2": {
            "sentiment": "BAJISTA",
            "confidence": 0.88
        },
        "https://test.agromate.com/trigo-export-3": {
            "sentiment": "ALCISTA",
            "confidence": 0.91
        }
    }
    
    try:
        results = repo.upsert_news(test_news, sentiment_data)
        
        print(f"✅ Successfully upserted {len(results)} articles!\n")
        
        print("📊 Upserted Records:\n")
        for i, record in enumerate(results, 1):
            print(f"   [{i}] ID: {record['id']}")
            print(f"       Title: {record['title'][:60]}...")
            print(f"       Sentiment: {record.get('sentiment', 'N/A')} "
                  f"(confidence: {record.get('confidence', 'N/A')})")
            print(f"       Created: {record['created_at']}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to upsert: {e}\n")
        return
    
    print("-" * 80 + "\n")
    
    # Step 5: Test duplicate prevention (upsert same URLs again)
    print("🔄 Step 5: Testing duplicate prevention (upserting again)...\n")
    
    try:
        # Modify titles slightly but keep same URLs
        test_news[0].title = "Test UPDATED: Soja alcanza precios récord en Chicago"
        
        results = repo.upsert_news(test_news, sentiment_data)
        
        print(f"✅ Upsert successful! URLs updated, no duplicates created.\n")
        print(f"   Records returned: {len(results)}\n")
        
    except Exception as e:
        print(f"❌ Failed to test duplicates: {e}\n")
    
    print("-" * 80 + "\n")
    
    # Step 6: Query recent news
    print("🔍 Step 6: Querying recent news...\n")
    
    try:
        recent_news = repo.get_recent(hours=24, limit=10)
        
        print(f"✅ Found {len(recent_news)} recent articles (last 24h)\n")
        
        for i, article in enumerate(recent_news[:5], 1):
            print(f"   [{i}] {article['title'][:60]}...")
            print(f"       Source: {article['source']}")
            print(f"       Sentiment: {article.get('sentiment', 'N/A')}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to query: {e}\n")
    
    print("-" * 80 + "\n")
    
    # Step 7: Get sentiment statistics
    print("📈 Step 7: Getting sentiment statistics...\n")
    
    try:
        stats = repo.count_by_sentiment()
        
        print("Sentiment Distribution:\n")
        print(f"   🟢 ALCISTA:  {stats.get('ALCISTA', 0):3d} articles")
        print(f"   🔴 BAJISTA:  {stats.get('BAJISTA', 0):3d} articles")
        print(f"   ⚪ NEUTRAL:  {stats.get('NEUTRAL', 0):3d} articles")
        print(f"   ❓ NULL:     {stats.get('NULL', 0):3d} articles")
        print()
        
    except Exception as e:
        print(f"❌ Failed to get stats: {e}\n")
    
    print("="*80)
    print("✅ Database test completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(test_database_connection())
