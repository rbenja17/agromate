"""Service to fetch market data from Yahoo Finance."""

import logging
import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

from scrapers.market_scraper import AgrofyMarketScraper

class MarketDataService:
    """Service to fetch market data for agricultural commodities."""
    
    # Mapping of simplified internal keys to Yahoo Finance tickers (ONLY FOR USD)
    TICKERS = {
        "dolar": "ARS=X"      # USD/ARS Exchange Rate
    }
    
    @classmethod
    async def get_latest_prices(cls) -> Dict[str, Any]:
        """
        Fetch latest prices: Grains from Agrofy, Dollar from Yahoo.
        """
        results = {}
        
        try:
            # 1. Fetch Dollar from Yahoo Finance (Fast & Reliable for FX)
            try:
                # Download just USD
                data = yf.download("ARS=X", period="5d", progress=False)
                if not data.empty:
                    # Series handling
                    series = data['Close']
                    if isinstance(series, pd.DataFrame): # Handle multi-index if single ticker sometimes returns weird
                         series = series.iloc[:, 0]
                         
                    last_price = float(series.dropna().iloc[-1])
                    prev_price = float(series.dropna().iloc[-2] if len(series.dropna()) > 1 else last_price)
                    change = ((last_price - prev_price) / prev_price) * 100
                    
                    results["dolar"] = {
                        "price": round(last_price, 2),
                        "currency": "ARS",
                        "change_percent": round(change, 2),
                        "symbol": "USD/ARS",
                        "name": "Dólar Oficial"
                    }
            except Exception as e:
                logger.error(f"Yahoo Finance Error: {e}")
                results["dolar"] = {"error": "unavailable", "symbol": "USD/ARS"}

            # 2. Fetch Grains from Agrofy (Real Local Prices)
            agrofy_data = await AgrofyMarketScraper.get_prices()
            if not agrofy_data:
                # Fallback to mock if scrape fails
                agrofy_data = AgrofyMarketScraper.get_mock_agrofy_data()
            
            results.update(agrofy_data)
                    
            return {
                "timestamp": str(datetime.utcnow()), # Use dynamic timestamp
                "data": results
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch market data: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_mock_data() -> Dict[str, Any]:
        """Return distinct mock data if API fails."""
        return {
            "timestamp": "MOCK",
            "data": {
                "soja_cbot": {"price": 1205.50, "currency": "USD", "change_percent": 1.2, "symbol": "ZS=F"},
                "maiz_cbot": {"price": 450.25, "currency": "USD", "change_percent": -0.5, "symbol": "ZC=F"},
                "trigo_cbot": {"price": 580.00, "currency": "USD", "change_percent": 0.1, "symbol": "ZW=F"},
                "dolar": {"price": 1250.00, "currency": "ARS", "change_percent": 0.0, "symbol": "ARS=X"}
            }
        }
