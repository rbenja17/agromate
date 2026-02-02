# Sentiment Analysis Module

Módulo de análisis de sentimiento para noticias agropecuarias de Agromate.

## 📁 Estructura

```
sentiment/
├── __init__.py          # Exports del módulo
├── llm_client.py        # Cliente LLM (Mock y Real)
└── analyzer.py          # Analizador de sentimiento
```

## 🤖 MockLLMClient

Cliente simulado que genera clasificaciones de sentimiento sin necesidad de API keys.

### Características

- ✅ Sentimientos aleatorios: `ALCISTA`, `BAJISTA`, `NEUTRAL`
- ✅ Scores de confianza realistas (0.70 - 0.99)
- ✅ Latencia de red simulada (configurable)
- ✅ Modo batch para múltiples textos

### Uso

```python
from sentiment import MockLLMClient

# Initialize client
client = MockLLMClient(simulate_latency=True, latency_seconds=0.5)

# Analyze single text
result = client.analyze("Soja sube 5% en la bolsa de Chicago")
print(result)
# {'sentiment': 'ALCISTA', 'confidence': 0.92}

# Batch analysis
results = client.analyze_batch([
    "Sequía afecta campos de maíz",
    "Exportaciones récord de trigo"
])
```

## 📊 SentimentAnalyzer

Procesa noticias y las enriquece con análisis de sentimiento.

### Características

- ✅ Procesa objetos `News` del modelo
- ✅ Análisis individual o batch
- ✅ Estadísticas agregadas de sentimiento
- ✅ Manejo de errores robusto
- ✅ Logging detallado

### Uso

```python
from sentiment import SentimentAnalyzer, MockLLMClient
from models.news import News

# Initialize analyzer (auto-creates MockLLMClient if not provided)
analyzer = SentimentAnalyzer()

# Or with custom client
custom_client = MockLLMClient(latency_seconds=0.1)
analyzer = SentimentAnalyzer(llm_client=custom_client)

# Analyze news
news_items = [
    News(title="Soja alcanza máximo histórico", source="Agro", url="https://...", published_at=None),
    News(title="Sequía amenaza cosecha", source="Campo", url="https://...", published_at=None)
]

enriched = analyzer.analyze_news(news_items)

for item in enriched:
    print(f"{item['title']}")
    print(f"  Sentiment: {item['sentiment']} ({item['confidence']})")
```

### Estadísticas

```python
# Get aggregated statistics
summary = analyzer.get_sentiment_summary(enriched)

print(f"Total: {summary['total']}")
print(f"Alcista: {summary['alcista']['count']} ({summary['alcista']['percentage']}%)")
print(f"Bajista: {summary['bajista']['count']} ({summary['bajista']['percentage']}%)")
print(f"Neutral: {summary['neutral']['count']} ({summary['neutral']['percentage']}%)")
```

## 🧪 Testing

### Script de Prueba

El script `test_sentiment.py` integra scraping + análisis:

```powershell
.\venv\Scripts\python test_sentiment.py
```

### Salida Esperada

```
================================================================================
🌾 AGROMATE - Sentiment Analysis Test
================================================================================

📰 Step 1: Scraping news from Bichos de Campo...
✅ Scraped 5 articles for testing

🤖 Step 2: Analyzing sentiment (using Mock LLM)...

📊 Step 3: Sentiment Analysis Results
================================================================================

[1] Dólar Blue en Córdoba: precio y cotización de este 31 enero...
    🟢 ALCISTA (confidence: 0.87)
    📅 2026-01-31 14:35:08
    🔗 https://bichosdecampo.com/...

[2] Sequía afecta la producción de maíz en la región...
    🔴 BAJISTA (confidence: 0.91)
    📅 2026-01-31 13:20:15
    🔗 https://bichosdecampo.com/...

================================================================================
📈 Sentiment Summary

Total analyzed: 5 articles

🟢 ALCISTA:   2 ( 40.0%)
🔴 BAJISTA:   1 ( 20.0%)
⚪ NEUTRAL:   2 ( 40.0%)

================================================================================
✅ Sentiment analysis test completed!
================================================================================
```

## 🔮 Migración a LLM Real

Cuando tengas una API key, podrás crear un `RealLLMClient`:

```python
# sentiment/llm_client.py

class RealLLMClient:
    """Real LLM client using OpenAI/Claude API."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def analyze(self, text: str) -> Dict[str, any]:
        prompt = f"""
        Analiza el siguiente titular de noticia agropecuaria argentina 
        y clasifica su impacto en el precio de la SOJA como:
        - ALCISTA (positivo para el precio)
        - BAJISTA (negativo para el precio)
        - NEUTRAL (sin impacto claro)
        
        Titular: "{text}"
        
        Responde en formato JSON: {{"sentiment": "...", "confidence": 0.XX}}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.choices[0].message.content)
```

Luego simplemente:

```python
from sentiment import SentimentAnalyzer, RealLLMClient

real_client = RealLLMClient(api_key=os.getenv("OPENAI_API_KEY"))
analyzer = SentimentAnalyzer(llm_client=real_client)
```

## 📊 Formato de Output

### Noticia Enriquecida

```python
{
    # Original news data
    "title": "Soja alcanza máximo histórico en Chicago",
    "source": "Bichos de Campo",
    "url": "https://bichosdecampo.com/...",
    "published_at": datetime(2026, 1, 31, 14, 35, 8),
    
    # Sentiment analysis
    "sentiment": "ALCISTA",
    "confidence": 0.92
}
```

### Resumen Estadístico

```python
{
    "total": 10,
    "alcista": {
        "count": 4,
        "percentage": 40.0
    },
    "bajista": {
        "count": 3,
        "percentage": 30.0
    },
    "neutral": {
        "count": 3,
        "percentage": 30.0
    },
    "errors": 0
}
```

## ✨ Características Implementadas

- ✅ MockLLMClient con sentimientos aleatorios
- ✅ SentimentAnalyzer para procesar noticias
- ✅ Análisis individual y batch
- ✅ Estadísticas agregadas
- ✅ Manejo de errores
- ✅ Logging completo
- ✅ Test script funcional con emojis
- ✅ Listo para migrar a LLM real

---

**Status:** ✅ Fase 3 completada  
**Test:** ✅ 5 artículos analizados exitosamente  
**Siguiente:** Integración con Supabase (Fase 4)
