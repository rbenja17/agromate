"""
Re-analizar todas las noticias existentes con el nuevo prompt mejorado de Groq.
Esto permite ver las llamadas a Groq y verificar la mejora en la categorización.
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

print("🔄 Re-analizando noticias con el nuevo prompt de Groq...")
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
        
        # Re-analizar con Groq
        analysis = llm_client.analyze(title, source)
        new_sentiment = analysis['sentiment']
        new_confidence = analysis['confidence']
        reasoning = analysis.get('reasoning', 'N/A')
        
        # Actualizar en BD
        supabase.table("news").update({
            'sentiment': new_sentiment,
            'confidence': new_confidence
        }).eq('id', news['id']).execute()
        
        # Mostrar resultado
        change_indicator = "✅" if old_sentiment == new_sentiment else "🔄"
        print(f"{change_indicator} [{i}/10] {source}")
        print(f"   {old_sentiment} → {new_sentiment} ({new_confidence})")
        print(f"   \"{title[:80]}...\"")
        print(f"   Razón: {reasoning}\n")
        
    except Exception as e:
        print(f"❌ Error en noticia {i}: {e}\n")

print("\n✅ Re-análisis completado!")
print("🔍 Revisá el dashboard de Groq - deberías ver ~10 llamadas nuevas")
