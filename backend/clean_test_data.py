"""
Script para limpiar datos de prueba de Supabase.
Elimina todas las noticias de "Test Source" y otras fuentes no productivas.
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

print("🗑️  Limpiando datos de prueba de Supabase...")

# Eliminar todas las noticias de "Test Source"
result = supabase.table("news").delete().eq("source", "Test Source").execute()
print(f"✅ Eliminadas {len(result.data)} noticias de 'Test Source'")

# Opcional: Eliminar TODAS las noticias para empezar limpio
# Descomenta si querés borrar todo:
# result = supabase.table("news").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
# print(f"✅ Base de datos limpiada: {len(result.data)} noticias eliminadas")

print("\n📊 Conteo actual por fuente:")
result = supabase.table("news").select("source").execute()
sources = {}
for row in result.data:
    source = row['source']
    sources[source] = sources.get(source, 0) + 1

for source, count in sorted(sources.items()):
    print(f"  {source}: {count} noticias")

print(f"\n✅ Total: {len(result.data)} noticias en la base de datos")
