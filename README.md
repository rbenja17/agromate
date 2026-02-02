# 🌾 Agromate - Análisis de Sentimiento del Mercado Agropecuario

MVP de herramienta de análisis de sentimiento para el mercado agropecuario argentino (Matba Rofex).

## 📊 Descripción

Agromate analiza titulares de noticias del sector agropecuario argentino y los clasifica como **Alcista**, **Bajista** o **Neutral** para commodities (comenzando con Soja). La herramienta utiliza scraping de fuentes RSS y procesamiento con LLM para generar insights de mercado.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js App   │────▶│  FastAPI Backend│────▶│    Supabase     │
│   (Dashboard)   │◀────│  (API + Scraper)│◀────│   (PostgreSQL)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   LLM Service   │
                        │   (Simulado)    │
                        └─────────────────┘
```

---

## 📁 Estructura de Directorios

```
Agromate/
├── README.md
├── .env.example
├── .gitignore
│
├── backend/                          # Python FastAPI Backend
│   ├── requirements.txt
│   ├── main.py                       # Entry point FastAPI
│   ├── config.py                     # Configuración y variables de entorno
│   │
│   ├── scrapers/                     # Módulo de Scraping RSS
│   │   ├── __init__.py
│   │   ├── base_scraper.py           # Clase base para scrapers
│   │   ├── rss_scraper.py            # Scraper genérico RSS
│   │   └── sources.py                # Definición de fuentes RSS
│   │
│   ├── sentiment/                    # Módulo de Análisis de Sentimiento
│   │   ├── __init__.py
│   │   ├── analyzer.py               # Lógica principal de análisis
│   │   └── llm_client.py             # Cliente LLM (simulado/real)
│   │
│   ├── models/                       # Modelos Pydantic
│   │   ├── __init__.py
│   │   ├── news.py                   # Modelo de noticia
│   │   └── sentiment.py              # Modelo de sentimiento
│   │
│   ├── database/                     # Capa de Datos
│   │   ├── __init__.py
│   │   ├── supabase_client.py        # Cliente Supabase
│   │   └── repositories.py           # Repositorios de datos
│   │
│   └── routers/                      # Endpoints API
│       ├── __init__.py
│       ├── news.py                   # Endpoints de noticias
│       └── health.py                 # Health check
│
├── frontend/                         # Next.js Dashboard
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   │
│   ├── src/
│   │   ├── app/                      # App Router (Next.js 14+)
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx              # Dashboard principal
│   │   │   └── globals.css
│   │   │
│   │   ├── components/               # Componentes React
│   │   │   ├── NewsCard.tsx          # Card de noticia individual
│   │   │   ├── NewsList.tsx          # Lista de noticias
│   │   │   ├── SentimentBadge.tsx    # Badge de sentimiento
│   │   │   └── Header.tsx            # Header del dashboard
│   │   │
│   │   ├── lib/                      # Utilidades
│   │   │   └── api.ts                # Cliente API
│   │   │
│   │   └── types/                    # TypeScript Types
│   │       └── index.ts
│   │
│   └── public/                       # Assets estáticos
│       └── logo.svg
│
└── supabase/                         # Configuración Supabase
    └── migrations/
        └── 001_create_news_table.sql # Schema inicial
```

---

## 🚀 Plan de Ejecución

### Fase 1: Setup Inicial (Est. 2 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 1.1 | Crear estructura de directorios | Generar carpetas según el árbol definido |
| 1.2 | Inicializar proyecto Python | `python -m venv venv`, crear `requirements.txt` |
| 1.3 | Inicializar proyecto Next.js | `npx create-next-app@latest frontend --typescript --tailwind --app` |
| 1.4 | Configurar Supabase | Crear proyecto en Supabase, obtener API keys |
| 1.5 | Crear archivos de configuración | `.env.example`, `.gitignore` |

---

### Fase 2: Backend - Scraping RSS (Est. 3 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 2.1 | Definir fuentes RSS | Configurar URLs de Bichos de Campo, Agrofynews, etc. |
| 2.2 | Implementar `base_scraper.py` | Clase base abstracta para scrapers |
| 2.3 | Implementar `rss_scraper.py` | Parser de feeds RSS usando `feedparser` |
| 2.4 | Crear modelo `News` | Pydantic model con campos: título, fuente, fecha, URL |
| 2.5 | Test unitario scraper | Verificar parsing correcto de feeds |

**Fuentes RSS Propuestas:**
- 🌾 Bichos de Campo: `https://bichosdecampo.com/feed/`
- 📰 Agrofynews: `https://news.agrofy.com.ar/rss.xml`
- 🌱 Infocampo: `https://www.infocampo.com.ar/feed/`

---

### Fase 3: Backend - Módulo de Sentimiento (Est. 2 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 3.1 | Crear `llm_client.py` | Cliente simulado que responde con sentimientos aleatorios |
| 3.2 | Implementar `analyzer.py` | Lógica para procesar noticias y obtener sentimiento |
| 3.3 | Definir prompt para LLM | Template optimizado para clasificación de commodities |
| 3.4 | Modelo `Sentiment` | Enum: ALCISTA, BAJISTA, NEUTRAL + confidence score |

**Prompt Template (para futuro LLM real):**
```
Analiza el siguiente titular de noticia agropecuaria argentina y clasifica 
su impacto en el precio de la SOJA como: ALCISTA, BAJISTA o NEUTRAL.

Titular: "{headline}"

Responde SOLO con: ALCISTA, BAJISTA o NEUTRAL
```

---

### Fase 4: Backend - Base de Datos (Est. 2 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 4.1 | Crear migración SQL | Tabla `news` con campos necesarios |
| 4.2 | Implementar `supabase_client.py` | Conexión a Supabase |
| 4.3 | Crear `repositories.py` | CRUD operations para noticias |
| 4.4 | Agregar índices | Por fecha y sentimiento |

**Schema SQL:**
```sql
CREATE TABLE news (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMPTZ,
    sentiment VARCHAR(20), -- 'ALCISTA', 'BAJISTA', 'NEUTRAL'
    confidence DECIMAL(3,2),
    commodity VARCHAR(50) DEFAULT 'SOJA',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_news_published_at ON news(published_at DESC);
CREATE INDEX idx_news_sentiment ON news(sentiment);
```

---

### Fase 5: Backend - API REST (Est. 2 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 5.1 | Crear `main.py` | Inicializar FastAPI, CORS, routers |
| 5.2 | Implementar `/api/news` | GET lista de noticias con filtros |
| 5.3 | Implementar `/api/news/refresh` | POST trigger manual de scraping |
| 5.4 | Implementar `/api/health` | Health check endpoint |
| 5.5 | Documentación OpenAPI | Automática via FastAPI |

**Endpoints:**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/news` | Lista noticias (paginadas, filtro por sentimiento) |
| GET | `/api/news/{id}` | Detalle de noticia |
| POST | `/api/news/refresh` | Ejecutar scraping manual |
| GET | `/api/health` | Estado del servicio |

---

### Fase 6: Frontend - Dashboard (Est. 4 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 6.1 | Setup Next.js | Configurar proyecto con App Router |
| 6.2 | Crear `api.ts` | Cliente para consumir backend |
| 6.3 | Implementar `NewsCard` | Componente visual de noticia |
| 6.4 | Implementar `SentimentBadge` | Badge con colores según sentimiento |
| 6.5 | Implementar `NewsList` | Lista scrollable de noticias |
| 6.6 | Crear página principal | Dashboard con header y lista |
| 6.7 | Estilizado | UI moderna y responsive |

**Diseño Visual:**
- 🟢 **Alcista:** Badge verde con icono ↑
- 🔴 **Bajista:** Badge rojo con icono ↓
- ⚪ **Neutral:** Badge gris con icono ↔

---

### Fase 7: Integración y Testing (Est. 2 horas)

| Paso | Tarea | Detalle |
|------|-------|---------|
| 7.1 | Conectar frontend con backend | Verificar llamadas API |
| 7.2 | Test end-to-end | Scraping → Análisis → Visualización |
| 7.3 | Manejo de errores | Loading states, error boundaries |
| 7.4 | README final | Instrucciones de instalación y uso |

---

## ⚙️ Requirements

### Backend (`backend/requirements.txt`)
```
fastapi==0.109.0
uvicorn==0.27.0
feedparser==6.0.10
supabase==2.3.0
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.26.0
```

### Frontend (`frontend/package.json`)
```json
{
  "dependencies": {
    "next": "14.x",
    "react": "18.x",
    "react-dom": "18.x",
    "typescript": "5.x"
  }
}
```

---

## 🔧 Variables de Entorno

```env
# Backend
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGc...
LLM_API_KEY=sk-...  # Para futuro LLM real

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📅 Timeline Estimado

| Fase | Duración | Acumulado |
|------|----------|-----------|
| Fase 1: Setup | 2h | 2h |
| Fase 2: Scraping | 3h | 5h |
| Fase 3: Sentimiento | 2h | 7h |
| Fase 4: Base de Datos | 2h | 9h |
| Fase 5: API REST | 2h | 11h |
| Fase 6: Frontend | 4h | 15h |
| Fase 7: Integración | 2h | **17h** |

**Total estimado: ~17 horas de desarrollo**

---

## 🔮 Roadmap Futuro (Post-MVP)

1. **Integración LLM Real** - OpenAI GPT-4 / Claude para análisis real
2. **Más Commodities** - Maíz, Trigo, Girasol
3. **Alertas** - Notificaciones push al detectar cambios de sentimiento
4. **Históricos** - Gráficos de tendencia de sentimiento
5. **Scraping avanzado** - Más fuentes, Twitter/X, informes de USDA
6. **API Pública** - Endpoints para terceros

---

## 👤 Autor

**Proyecto:** Agromate MVP  
**Stack:** Next.js + FastAPI + Supabase  
**Mercado:** Matba Rofex - Argentina

---

*Documento generado como plan de implementación. Código a desarrollar en fases siguientes.*
