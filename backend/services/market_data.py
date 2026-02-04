"""Service to fetch market data from Yahoo Finance."""

import logging
import yfinance as yf
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service to fetch market data for agricultural commodities."""
    
    # Mapping of simplified internal keys to Yahoo Finance tickers
    TICKERS = {
        "soja_cbot": "ZS=F",  # Soybean Futures
        "maiz_cbot": "ZC=F",  # Corn Futures
        "trigo_cbot": "ZW=F", # Wheat Futures
        "dolar": "ARS=X"      # USD/ARS Exchange Rate
    }
    
    @classmethod
    def get_latest_prices(cls) -> Dict[str, Any]:
        """
        Fetch latest prices for monitored commodities.
        
        Returns:
            Dictionary with commodity data.
        """
        results = {}
        
        try:
            # Join tickers with space for bulk download
            tickers_str = " ".join(cls.TICKERS.values())
            
            # Download recent data (last 5 days to ensure we get last close)
            # group_by='ticker' ensures we get a structure we can iterate easily
            data = yf.download(tickers_str, period="5d", group_by='column', progress=False)
            
            # Process each mapped ticker
            for name, symbol in cls.TICKERS.items():
                try:
                    # Extract Close series for the symbol
                    # yfinance structure varies by version, handling potential multi-index
                    # Usually: data['Close'][symbol]
                    
                    if symbol in data['Close']:
                        series = data['Close'][symbol]
                    else:
                        # Fallback if structure is different or flat
                        # Try to re-fetch single if bulk failed structure
                        ticker_data = yf.Ticker(symbol)
                        hist = ticker_data.history(period="5d")
                        series = hist['Close']
                        
                    # Get last valid value
                    last_price = series.dropna().iloc[-1]
                    # Get previous close for change calc
                    prev_price = series.dropna().iloc[-2] if len(series.dropna()) > 1 else last_price
                    
                    change = ((last_price - prev_price) / prev_price) * 100
                    
                    results[name] = {
                        "price": round(float(last_price), 2),
                        "currency": "USD" if name != "dolar" else "ARS",
                        "change_percent": round(float(change), 2),
                        "symbol": symbol
                    }
                    
                except Exception as e:
                    logger.error(f"Error processing {name} ({symbol}): {e}")
                    results[name] = {"error": "unavailable", "symbol": symbol}
                    
            return {
                "timestamp": str(data.index[-1]),
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
