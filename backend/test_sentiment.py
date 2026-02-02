"""Test script for sentiment analysis with Groq."""

import sys
from pathlib import Path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import asyncio
import logging
from dotenv import load_dotenv
load_dotenv()

from scrapers import RSScraper
from sentiment import SentimentAnalyzer
from sentiment.llm_client import GroqLLMClient, MockLLMClient, get_llm_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SENTIMENT_EMOJI = {"ALCISTA": "🟢", "BAJISTA": "🔴", "NEUTRAL": "⚪"}


async def test_groq_directly():
    """Test Groq LLM client directly."""
    print("\n" + "="*60)
    print("🤖 Test Directo de Groq (llama3-70b-8192)")
    print("="*60 + "\n")
    
    try:
        client = GroqLLMClient()
        print("✅ Cliente Groq inicializado\n")
        
        headlines = [
            ("Sequía severa afecta cultivos de soja en Buenos Aires", "Infocampo"),
            ("Cosecha récord de trigo proyectada para 2026", "Clarín Rural"),
            ("China aumenta demanda de soja argentina", "Reuters"),
        ]
        
        for i, (headline, source) in enumerate(headlines, 1):
            result = client.analyze(headline, source)
            emoji = SENTIMENT_EMOJI.get(result["sentiment"], "❓")
            print(f"[{i}] {headline}")
            print(f"    {emoji} {result['sentiment']} ({result['confidence']})")
            print()
        
        print("✅ Test completado!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_full_pipeline():
    """Test with real scraped news."""
    print("\n" + "="*60)
    print("🌾 Test Pipeline Completo")
    print("="*60 + "\n")
    
    # Scrape
    scraper = RSScraper(source_name="Bichos de Campo")
    news = await scraper.scrape("https://bichosdecampo.com/feed/")
    sample = news[:3]
    print(f"📰 Scrapeadas {len(sample)} noticias\n")
    
    # Analyze
    llm = get_llm_client(use_mock=False)
    analyzer = SentimentAnalyzer(llm_client=llm)
    results = analyzer.analyze_news(sample)
    
    # Display
    for i, item in enumerate(results, 1):
        emoji = SENTIMENT_EMOJI.get(item["sentiment"], "❓")
        title = item["title"][:50] + "..." if len(item["title"]) > 50 else item["title"]
        print(f"[{i}] {title}")
        print(f"    {emoji} {item['sentiment']} ({item['confidence']})")
        print()
    
    # Summary
    summary = analyzer.get_sentiment_summary(results)
    print(f"\n📊 Resumen: {summary['total']} noticias")
    print(f"🟢 Alcistas: {summary['alcista']['count']}")
    print(f"🔴 Bajistas: {summary['bajista']['count']}")
    print(f"⚪ Neutrales: {summary['neutral']['count']}")


if __name__ == "__main__":
    asyncio.run(test_groq_directly())
    asyncio.run(test_full_pipeline())
