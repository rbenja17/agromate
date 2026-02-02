# Agromate Backend

Backend en Python para scraping y análisis de noticias agropecuarias argentinas.

## 📋 Fases Completadas: Fase 1, 2 y 3

### ✅ Archivos Creados

```
backend/
├── requirements.txt         # Dependencias Python
├── models/
│   ├── __init__.py
│   └── news.py             # Modelo News (dataclass)
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # Clase base abstracta
│   ├── rss_scraper.py       # Implementación RSS
│   └── sources.py          # Fuentes RSS configuradas
├── sentiment/              # ✨ NUEVO en Fase 3
│   ├── __init__.py
│   ├── llm_client.py        # MockLLMClient
│   ├── analyzer.py          # SentimentAnalyzer
│   └── README.md           # Documentación del módulo
├── test_scraper.py          # Script de prueba scraping
├── test_sentiment.py        # ✨ NUEVO: Script de prueba sentiment
└── .env.example            # Template de variables de entorno
```

## 🚀 Instalación

### 1. Crear entorno virtual

```powershell
python -m venv venv
```

### 2. Activar entorno virtual

```powershell
.\venv\Scripts\Activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## 📰 Fuentes RSS Configuradas

| Fuente | URL | Status |
|--------|-----|--------|
| 🌾 Bichos de Campo | `https://bichosdecampo.com/feed/` | ✅ Activa |
| 📰 Agrofynews | `https://news.agrofy.com.ar/rss.xml` | ✅ Activa |
| 🌱 Infocampo | `https://www.infocampo.com.ar/feed/` | ✅ Activa |

## 🧪 Testing

### Ejecutar test del scraper

```powershell
.\venv\Scripts\python test_scraper.py
```

**Salida esperada:**
```
================================================================================
🌾 AGROMATE - RSS Scraper Test
================================================================================

📰 Testing: Bichos de Campo
   URL: https://bichosdecampo.com/feed/
--------------------------------------------------------------------------------
✅ Success! Found 16 articles

   [1] Título de la noticia...
       📅 2026-01-31 14:35:08
       🔗 https://...

🎯 Total articles scraped: 26
================================================================================
```

### Ejecutar test de análisis de sentimiento

```powershell
.\venv\Scripts\python test_sentiment.py
```

**Salida esperada:**
```
================================================================================
🌾 AGROMATE - Sentiment Analysis Test
================================================================================

📰 Step 1: Scraping news from Bichos de Campo...
✅ Scraped 5 articles for testing

🤖 Step 2: Analyzing sentiment (using Mock LLM)...

📊 Step 3: Sentiment Analysis Results
================================================================================

[1] Dólar Blue en Córdoba: precio y cotización...
    🟢 ALCISTA (confidence: 0.87)
    📅 2026-01-31 14:35:08
    🔗 https://bichosdecampo.com/...

📈 Sentiment Summary
Total analyzed: 5 articles

🟢 ALCISTA:   2 ( 40.0%)
🔴 BAJISTA:   1 ( 20.0%)
⚪ NEUTRAL:   2 ( 40.0%)
================================================================================
```

## 💻 Uso Programático

```python
import asyncio
from scrapers import RSScraper, get_active_sources

async def main():
    # Scraping una fuente específica
    scraper = RSScraper(source_name="Bichos de Campo")
    news_items = await scraper.scrape("https://bichosdecampo.com/feed/")
    
    for article in news_items:
        print(f"{article.title}")
        print(f"  Fuente: {article.source}")
        print(f"  URL: {article.url}")
        print(f"  Fecha: {article.published_at}")

asyncio.run(main())
```

## 📦 Modelo de Datos

### News Dataclass

```python
@dataclass
class News:
    title: str                           # Título de la noticia
    source: str                          # Nombre de la fuente
    url: str                             # URL del artículo
    published_at: Optional[datetime]     # Fecha de publicación
```

## 🔧 Configuración

### Agregar nueva fuente RSS

Editar `scrapers/sources.py`:

```python
RSS_SOURCES.append({
    "name": "Nueva Fuente",
    "url": "https://nuevafuente.com/feed/",
    "enabled": True,
})
```

### Deshabilitar una fuente

Cambiar `enabled` a `False` en `scrapers/sources.py`.

## 🧩 Arquitectura

### BaseScraper (Clase Abstracta)

Define la interfaz que todos los scrapers deben implementar:
- Método abstracto: `async def scrape(self, url: str) -> List[News]`
- Logging automático

### RSScraper (Implementación)

Características:
- ✅ Parseo de feeds RSS/Atom
- ✅ Normalización de fechas múltiples formatos
- ✅ Manejo robusto de errores
- ✅ Validación de entradas
- ✅ Logging detallado

## 📚 Dependencias Instaladas

- **fastapi** (0.115.0) - Framework web (para futura API)
- **uvicorn** (0.32.0) - Servidor ASGI
- **feedparser** (6.0.11) - Parser de feeds RSS
- **pydantic** (1.10.18) - Validación de datos
- **python-dotenv** (1.0.1) - Variables de entorno
- **httpx** (0.27.2) - Cliente HTTP async

## ✨ Características Implementadas

### Fase 1 y 2: Scraping
- ✅ Scraping asíncrono de múltiples fuentes RSS
- ✅ Modelo de datos validado (News dataclass)
- ✅ Manejo de errores robusto
- ✅ Normalización de fechas en múltiples formatos
- ✅ Logging estructurado
- ✅ Arquitectura extensible con clase base abstracta
- ✅ Test script funcional

### Fase 3: Análisis de Sentimiento
- ✅ MockLLMClient con sentimientos aleatorios
- ✅ SentimentAnalyzer para procesar noticias
- ✅ Clasificación: ALCISTA / BAJISTA / NEUTRAL
- ✅ Scores de confianza (0.70 - 0.99)
- ✅ Análisis individual y batch
- ✅ Estadísticas agregadas de sentimiento
- ✅ Test script integrado (scraping + análisis)
- ✅ Preparado para migrar a LLM real (OpenAI/Claude)

## 🔜 Próximos Pasos (Fase 4)

La siguiente fase incluirá:

1. **Integración con Supabase** (`database/`)
   - `supabase_client.py` - Cliente de conexión
   - `repositories.py` - CRUD operations
   - Migración SQL para tabla `news`

2. **Persistencia de Datos**
   - Guardar noticias scrapeadas
   - Almacenar análisis de sentimiento
   - Evitar duplicados por URL

---

**Status:** ✅ Fase 1, 2 y 3 completadas  
**Tests:** ✅ 26 artículos scrapeados + 5 analizados exitosamente  
**Siguiente:** Integración con Supabase (Base de Datos)
