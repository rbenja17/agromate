import asyncio
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from scrapers.market_scraper import AgrofyMarketScraper

async def test_agrofy():
    print("Fetching Agrofy prices...")
    try:
        data = await AgrofyMarketScraper.get_prices()
        print(f"Result: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_agrofy())
