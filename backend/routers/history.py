"""Historical market data endpoint."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/history")
async def get_market_history(
    days: int = Query(default=30, ge=1, le=90, description="Number of days of history"),
    commodity: str = Query(default="soja,maiz,trigo", description="Comma-separated commodity list")
):
    """
    Get historical price data for commodities and dollar.
    
    Returns daily close prices for CBOT futures + Dollar rates,
    suitable for charting.
    """
    try:
        import httpx
        
        commodities = [c.strip().lower() for c in commodity.split(",")]
        
        ticker_map = {
            "soja": {"symbol": "ZS=F", "name": "Soja (CBOT)"},
            "maiz": {"symbol": "ZC=F", "name": "Maíz (CBOT)"},
            "trigo": {"symbol": "ZW=F", "name": "Trigo (CBOT)"},
        }
        
        period = "1mo" if days <= 30 else "3mo"
        
        result = {
            "period": f"{days}d",
            "data": [],
            "commodities": []
        }
        
        # 1. Fetch grain futures from Yahoo Finance
        try:
            import yfinance as yf
            
            symbols_to_fetch = []
            for c in commodities:
                if c in ticker_map:
                    symbols_to_fetch.append(ticker_map[c]["symbol"])
            
            if symbols_to_fetch:
                symbols_str = " ".join(symbols_to_fetch)
                data = yf.download(symbols_str, period=period, progress=False, group_by="ticker")
                
                # Build date-indexed dict
                dates_dict = {}
                
                for c in commodities:
                    if c not in ticker_map:
                        continue
                    
                    sym = ticker_map[c]["symbol"]
                    result["commodities"].append({"key": c, "name": ticker_map[c]["name"]})
                    
                    try:
                        if len(symbols_to_fetch) > 1 and sym in data.columns.get_level_values(0):
                            series = data[sym]["Close"].dropna()
                        elif len(symbols_to_fetch) == 1:
                            series = data["Close"].dropna()
                        else:
                            continue
                        
                        for date_idx, price in series.items():
                            date_key = date_idx.strftime("%Y-%m-%d")
                            if date_key not in dates_dict:
                                dates_dict[date_key] = {"date": date_key}
                            # CBOT prices are in cents/bushel, convert to USD/ton
                            usd_per_bushel = float(price) / 100
                            usd_per_ton = usd_per_bushel * 36.744  # ~36.744 bushels per metric ton for soy
                            dates_dict[date_key][f"{c}_usd"] = round(usd_per_ton, 2)
                    except Exception as e:
                        logger.warning(f"Error parsing {c} history: {e}")
        except Exception as e:
            logger.error(f"Yahoo Finance history error: {e}")
        
        # 2. Fetch dollar history (from DolarAPI / ArgentinaDatos)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Current rates
                resp = await client.get("https://dolarapi.com/v1/dolares")
                if resp.status_code == 200:
                    dolar_data = resp.json()
                    oficial = next((d for d in dolar_data if d.get("casa", "").lower() == "oficial"), None)
                    blue = next((d for d in dolar_data if d.get("casa", "").lower() == "blue"), None)
                    
                    today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    if today_key not in dates_dict:
                        dates_dict[today_key] = {"date": today_key}
                    
                    if oficial:
                        dates_dict[today_key]["dolar_oficial"] = float(oficial.get("venta", 0))
                    if blue:
                        dates_dict[today_key]["dolar_blue"] = float(blue.get("venta", 0))
                    
                    # Calculate brecha
                    if oficial and blue:
                        of_val = float(oficial.get("venta", 1))
                        bl_val = float(blue.get("venta", 1))
                        dates_dict[today_key]["brecha_pct"] = round(((bl_val - of_val) / of_val) * 100, 2)
        except Exception as e:
            logger.warning(f"DolarAPI history error: {e}")
        
        # Convert to sorted list
        result["data"] = sorted(dates_dict.values(), key=lambda x: x["date"])
        
        # Limit to requested days
        result["data"] = result["data"][-days:]
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching market history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
