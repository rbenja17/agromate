"""Daily AI summary endpoint using Groq."""

import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException

from database import get_supabase_client, NewsRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/summary", tags=["summary"])


@router.get("/daily")
async def get_daily_summary():
    """
    Generate an AI-powered daily market summary.
    
    Takes today's news, calculates stats, and asks Groq to produce
    a 2-3 sentence market overview for Argentine agricultural producers.
    """
    try:
        client = get_supabase_client()
        repo = NewsRepository(client)
        
        # Get news from the last 24 hours
        all_news = repo.get_recent(hours=24, limit=200)
        
        if not all_news:
            # Fall back to most recent news regardless of date
            all_news = repo.get_all(limit=50)
        
        if not all_news:
            return {
                "summary": "No hay noticias disponibles para generar un resumen. Ejecutá 'Actualizar Análisis' para obtener datos.",
                "sentiment_score": 0.0,
                "stats": {"alcista": 0, "bajista": 0, "neutral": 0, "total": 0},
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        
        # Calculate stats
        alcista = sum(1 for n in all_news if (n.get('sentiment') or '').upper() == 'ALCISTA')
        bajista = sum(1 for n in all_news if (n.get('sentiment') or '').upper() == 'BAJISTA')
        neutral = sum(1 for n in all_news if (n.get('sentiment') or '').upper() == 'NEUTRAL')
        total = len(all_news)
        
        # Calculate weighted score
        score = 0.0
        if alcista + bajista > 0:
            score = (alcista - bajista) / (alcista + bajista)
        
        # Collect commodity mentions
        commodities = {}
        for n in all_news:
            c = n.get('commodity', 'GENERAL')
            if c and c != 'IRRELEVANT':
                commodities[c] = commodities.get(c, 0) + 1
        
        top_commodities = sorted(commodities.items(), key=lambda x: x[1], reverse=True)[:3]
        commodity_text = ", ".join(f"{c} ({n})" for c, n in top_commodities) if top_commodities else "sin datos"
        
        # Collect some example headlines
        headlines = [n.get('title', '') for n in all_news[:10]]
        headlines_text = "\n".join(f"- {h}" for h in headlines if h)
        
        # Generate summary via Groq
        summary_text = await _generate_summary_with_groq(
            alcista=alcista,
            bajista=bajista,
            neutral=neutral,
            total=total,
            score=score,
            commodity_text=commodity_text,
            headlines_text=headlines_text
        )
        
        return {
            "summary": summary_text,
            "sentiment_score": round(score, 2),
            "stats": {
                "alcista": alcista,
                "bajista": bajista,
                "neutral": neutral,
                "total": total
            },
            "top_commodities": dict(top_commodities),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating daily summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_summary_with_groq(
    alcista: int, bajista: int, neutral: int, total: int,
    score: float, commodity_text: str, headlines_text: str
) -> str:
    """Use Groq LLM to generate a natural language market summary."""
    try:
        from sentiment.llm_client import get_llm_client
        
        llm = get_llm_client(use_mock=False)
        
        prompt = f"""Eres un analista senior del mercado agropecuario argentino.

DATOS DEL DÍA:
- Total noticias analizadas: {total}
- Alcistas (precios suben): {alcista} ({round(alcista/total*100, 1) if total else 0}%)
- Bajistas (precios bajan): {bajista} ({round(bajista/total*100, 1) if total else 0}%)
- Neutrales: {neutral}
- Score de sentimiento: {score:.2f} (-1=muy bajista, +1=muy alcista)
- Commodities principales: {commodity_text}

TITULARES RECIENTES:
{headlines_text}

INSTRUCCIONES:
Genera un resumen de mercado EN ESPAÑOL de 2-3 oraciones para un productor agropecuario argentino.
- Sé conciso y profesional
- Menciona los commodities más relevantes
- Indica si el ánimo general es alcista, bajista o mixto
- Si hay alguna noticia particularmente relevante, mencionala
- NO uses JSON, solo texto plano
- NO uses más de 3 oraciones"""

        # Use Groq directly for text generation (not JSON mode)
        from groq import Groq
        import os
        
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Groq summary generation failed: {e}")
        # Generate a basic fallback summary
        if score > 0.2:
            mood = "predominantemente alcista"
        elif score < -0.2:
            mood = "predominantemente bajista"
        else:
            mood = "mixto/neutral"
        
        return (
            f"De {total} noticias analizadas, el sentimiento del mercado agropecuario es {mood} "
            f"(score: {score:.2f}). Se detectaron {alcista} noticias alcistas, "
            f"{bajista} bajistas y {neutral} neutrales. "
            f"Commodities destacados: {commodity_text}."
        )
