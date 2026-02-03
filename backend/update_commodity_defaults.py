"""
Cambiar el default de todas las noticias de SOJA a GENERAL.
Esto es más correcto porque la mayoría de noticias NO son específicas de soja.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Conectar a Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

print("🔄 Actualizando commodity default de SOJA a GENERAL...\n")

# Obtener todas las noticias con commodity = SOJA
result = supabase.table("news").select("id, title, commodity").eq("commodity", "SOJA").execute()
news_with_soja = result.data

print(f"📊 Encontradas {len(news_with_soja)} noticias con commodity=SOJA\n")

if len(news_with_soja) > 0:
    # Actualizar todas a GENERAL
    response = supabase.table("news").update({
        "commodity": "GENERAL"
    }).eq("commodity", "SOJA").execute()
    
    print(f"✅ Actualizadas {len(news_with_soja)} noticias a commodity=GENERAL")
    print("\n💡 Ahora cuando scrapeemos noticias nuevas, Groq detectará el commodity correcto.")
    print("💡 Si querés, podés re-analizar todas las noticias con el script test_commodity_detection.py")
else:
    print("✅ No hay noticias con commodity=SOJA para actualizar")

print("\n📊 Distribución actual por commodity:")
all_news = supabase.table("news").select("commodity").execute()
commodities = {}
for row in all_news.data:
    commodity = row.get('commodity', 'NULL')
    commodities[commodity] = commodities.get(commodity, 0) + 1

for commodity, count in sorted(commodities.items(), key=lambda x: x[1], reverse=True):
    print(f"  {commodity}: {count} noticias")
