"""Divergence detection: sentiment vs price mismatch (Behavioral Science)."""

import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from database import get_supabase_client, NewsRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["divergence"])


@router.get("/divergence")
async def get_divergence(
    commodity: str = Query(default="soja", description="Commodity to analyze"),
    days: int = Query(default=7, ge=1, le=30, description="Days to analyze")
):
    """
    Detect divergence between news sentiment and actual price movement.
    
    A divergence occurs when:
    - BULLISH DIVERGENCE: News are mostly alcista but CBOT price dropped
    - BEARISH DIVERGENCE: News are mostly bajista but CBOT price rose
    
    This signals potential market inefficiency or media bias.
    """
    try:
        # 1. Calculate sentiment score for the period
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        all_news = repo.get_filtered(
            commodity=commodity.upper() if commodity.upper() != "GENERAL" else None,
            date_from=start_date.isoformat(),
            limit=500
        )
        
        if not all_news:
            return {
                "divergence_type": "NONE",
                "message": f"No hay suficientes noticias sobre {commodity.upper()} en los últimos {days} días.",
                "sentiment_score": 0.0,
                "price_change_pct": 0.0,
                "signal_strength": 0,
                "description": ""
            }
        
        # Calculate weighted sentiment
        alcista = sum(1 for n in all_news if (n.get('sentiment') or '').upper() == 'ALCISTA')
        bajista = sum(1 for n in all_news if (n.get('sentiment') or '').upper() == 'BAJISTA')
        
        sentiment_score = 0.0
        if alcista + bajista > 0:
            sentiment_score = (alcista - bajista) / (alcista + bajista)
        
        # 2. Get price change from Yahoo Finance
        ticker_map = {
            "soja": "ZS=F",
            "maiz": "ZC=F",
            "trigo": "ZW=F",
        }
        
        symbol = ticker_map.get(commodity.lower())
        price_change_pct = 0.0
        
        if symbol:
            try:
                import yfinance as yf
                
                period = "1mo" if days <= 7 else "3mo"
                data = yf.download(symbol, period=period, progress=False)
                
                if len(data) >= 2:
                    recent = data["Close"].dropna()
                    if len(recent) >= days:
                        start_price = float(recent.iloc[-days])
                        end_price = float(recent.iloc[-1])
                        price_change_pct = ((end_price - start_price) / start_price) * 100
                    elif len(recent) >= 2:
                        start_price = float(recent.iloc[0])
                        end_price = float(recent.iloc[-1])
                        price_change_pct = ((end_price - start_price) / start_price) * 100
            except Exception as e:
                logger.warning(f"Yahoo Finance error for divergence: {e}")
        
        # 3. Detect divergence
        divergence_type = "NONE"
        description = ""
        signal_strength = 0  # 0-3 scale
        
        SENTIMENT_THRESHOLD = 0.25
        PRICE_THRESHOLD = 1.5  # percent
        
        if sentiment_score > SENTIMENT_THRESHOLD and price_change_pct < -PRICE_THRESHOLD:
            divergence_type = "BULLISH_DIVERGENCE"
            signal_strength = min(3, int(abs(sentiment_score * 3) + abs(price_change_pct / 3)))
            description = (
                f"⚠️ Las noticias sobre {commodity.upper()} son mayormente alcistas (score: {sentiment_score:.2f}), "
                f"pero el precio en Chicago BAJÓ {abs(price_change_pct):.1f}% en {days} días. "
                f"Esto puede indicar un sesgo mediático: el mercado no acompaña el optimismo de las noticias."
            )
        elif sentiment_score < -SENTIMENT_THRESHOLD and price_change_pct > PRICE_THRESHOLD:
            divergence_type = "BEARISH_DIVERGENCE"
            signal_strength = min(3, int(abs(sentiment_score * 3) + abs(price_change_pct / 3)))
            description = (
                f"⚠️ Las noticias sobre {commodity.upper()} son mayormente bajistas (score: {sentiment_score:.2f}), "
                f"pero el precio en Chicago SUBIÓ {price_change_pct:.1f}% en {days} días. "
                f"El mercado ignora el pesimismo mediático, posible oportunidad."
            )
        elif abs(sentiment_score) > SENTIMENT_THRESHOLD and abs(price_change_pct) < PRICE_THRESHOLD:
            divergence_type = "NEUTRAL_PRICE"
            description = (
                f"Las noticias sobre {commodity.upper()} muestran un sesgo "
                f"{'alcista' if sentiment_score > 0 else 'bajista'} "
                f"(score: {sentiment_score:.2f}), pero el precio se mantuvo estable "
                f"({price_change_pct:+.1f}%). Sin divergencia significativa."
            )
        else:
            description = (
                f"Sentimiento y precio de {commodity.upper()} están alineados. "
                f"Score: {sentiment_score:.2f}, Precio: {price_change_pct:+.1f}%."
            )
        
        return {
            "divergence_type": divergence_type,
            "commodity": commodity.upper(),
            "sentiment_score": round(sentiment_score, 2),
            "price_change_pct": round(price_change_pct, 2),
            "signal_strength": signal_strength,
            "news_count": len(all_news),
            "alcista_count": alcista,
            "bajista_count": bajista,
            "days_analyzed": days,
            "description": description
        }
        
    except Exception as e:
        logger.error(f"Error calculating divergence: {e}")
        raise HTTPException(status_code=500, detail=str(e))
