"""Service to fetch market data from public APIs (DolarAPI + Yahoo Finance)."""

import logging
from datetime import datetime
from typing import Dict, Any

import httpx

logger = logging.getLogger(__name__)


class MarketDataService:
    """Service to fetch real market data for agricultural commodities."""

    # DolarAPI endpoints (free, no auth, instant updates)
    DOLAR_API = "https://dolarapi.com/v1/dolares"

    @classmethod
    async def get_latest_prices(cls) -> Dict[str, Any]:
        """
        Fetch latest prices from real APIs:
        - Dollar: DolarAPI (oficial, blue, MEP)
        - Grains: Yahoo Finance futures (converted to ARS)
        """
        results = {}

        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. Fetch Dollar rates from DolarAPI (reliable, always works)
            try:
                resp = await client.get(cls.DOLAR_API)
                resp.raise_for_status()
                dolar_data = resp.json()

                for item in dolar_data:
                    casa = item.get("casa", "").lower()
                    if casa == "oficial":
                        results["dolar"] = {
                            "price": float(item.get("venta", 0)),
                            "currency": "ARS",
                            "change_percent": 0.0,
                            "symbol": "USD/ARS",
                            "name": "Dólar Oficial"
                        }
                    elif casa == "blue":
                        results["dolar_blue"] = {
                            "price": float(item.get("venta", 0)),
                            "currency": "ARS",
                            "change_percent": 0.0,
                            "symbol": "USD/ARS Blue",
                            "name": "Dólar Blue"
                        }
            except Exception as e:
                logger.error(f"DolarAPI error: {e}")
                results["dolar"] = {"error": "unavailable", "symbol": "USD/ARS"}

            # 2. Fetch Grain futures from Yahoo Finance (international ref)
            try:
                import yfinance as yf
                import pandas as pd

                tickers = {
                    "soja": {"symbol": "ZS=F", "name": "Soja (CBOT)"},
                    "maiz": {"symbol": "ZC=F", "name": "Maíz (CBOT)"},
                    "trigo": {"symbol": "ZW=F", "name": "Trigo (CBOT)"},
                }

                symbols = " ".join(t["symbol"] for t in tickers.values())
                data = yf.download(symbols, period="5d", progress=False, group_by="ticker")

                dolar_price = results.get("dolar", {}).get("price", 1200)

                for key, info in tickers.items():
                    try:
                        sym = info["symbol"]
                        if sym in data.columns.get_level_values(0):
                            series = data[sym]["Close"].dropna()
                        else:
                            series = data["Close"].dropna()

                        if len(series) > 0:
                            usd_cents = float(series.iloc[-1])
                            usd_price = usd_cents / 100  # CBOT quotes in cents/bushel
                            ars_price = round(usd_price * dolar_price, 2)

                            prev_cents = float(series.iloc[-2]) if len(series) > 1 else usd_cents
                            change = ((usd_cents - prev_cents) / prev_cents) * 100

                            results[f"{key}_rosario"] = {
                                "price": ars_price,
                                "currency": "ARS",
                                "change_percent": round(change, 2),
                                "symbol": sym,
                                "name": info["name"]
                            }
                    except Exception as e:
                        logger.warning(f"Error parsing {key}: {e}")

            except Exception as e:
                logger.error(f"Yahoo Finance error: {e}")

        # Fallback if nothing worked
        if not results:
            return cls.get_mock_data()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "data": results
        }

    @staticmethod
    def get_mock_data() -> Dict[str, Any]:
        """Return fallback mock data if all APIs fail."""
        return {
            "timestamp": "MOCK",
            "data": {
                "soja_rosario": {"price": 470000, "currency": "ARS", "change_percent": -1.26, "symbol": "ZS=F", "name": "Soja (CBOT)"},
                "maiz_rosario": {"price": 265000, "currency": "ARS", "change_percent": -3.01, "symbol": "ZC=F", "name": "Maíz (CBOT)"},
                "trigo_rosario": {"price": 259560, "currency": "ARS", "change_percent": 0.28, "symbol": "ZW=F", "name": "Trigo (CBOT)"},
                "dolar": {"price": 1200, "currency": "ARS", "change_percent": 0.0, "symbol": "USD/ARS", "name": "Dólar Oficial"}
            }
        }
