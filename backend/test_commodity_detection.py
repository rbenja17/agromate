"""
Re-analizar 10 noticias con el nuevo prompt que detecta commodity.
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from sentiment.llm_client import get_llm_client

load_dotenv()

# Conectar a Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Get Groq client
llm_client = get_llm_client(use_mock=False)

print("🌾 Re-analizando noticias para detectar commodities con Groq...")
print("⚠️  ESTO HARÁ LLAMADAS REALES A GROQ API\n")

# Obtener primeras 10 noticias para re-analizar
result = supabase.table("news").select("*").limit(10).execute()
news_items = result.data

print(f"📊 Analizando {len(news_items)} noticias...\n")

for i, news in enumerate(news_items, 1):
    try:
        title = news['title']
        source = news['source']
        old_sentiment = news['sentiment']
        old_commodity = news.get('commodity', 'SOJA')
        
        # Re-analizar con Groq
        analysis = llm_client.analyze(title, source)
        new_sentiment = analysis['sentiment']
        new_confidence = analysis['confidence']
        new_commodity = analysis.get('commodity', 'GENERAL')
        reasoning = analysis.get('reasoning', 'N/A')
        
        # Actualizar en BD
        supabase.table("news").update({
            'sentiment': new_sentiment,
            'confidence': new_confidence,
            'commodity': new_commodity
        }).eq('id', news['id']).execute()
        
        # Mostrar resultado
        commodity_changed = "🔄" if old_commodity != new_commodity else "✅"
        sentiment_changed = "🔄" if old_sentiment != new_sentiment else "✅"
        
        print(f"{sentiment_changed} [{i}/10] {source}")
        print(f"   Sentiment: {old_sentiment} → {new_sentiment} ({new_confidence})")
        print(f"   {commodity_changed} Commodity: {old_commodity} → {new_commodity}")
        print(f"   \"{title[:70]}...\"")
        print(f"   Razón: {reasoning}\n")
        
    except Exception as e:
        print(f"❌ Error en noticia {i}: {e}\n")

print("\n✅ Re-análisis completado!")
print("🔍 Revisá:")
print("   1. Dashboard de Groq → ~10 llamadas nuevas")
print("   2. Dashboard de Agromate → Filtro de Commodity activo")
