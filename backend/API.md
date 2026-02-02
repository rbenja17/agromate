# Agromate API - Guía de Uso

API REST para el backend de Agromate - Análisis de sentimiento del mercado agropecuario argentino.

## 🚀 Inicio Rápido

### 1. Levantar el servidor

```powershell
cd backend
.\venv\Scripts\python run_server.py
```

El servidor estará disponible en:
- **API:** http://localhost:8000
- **Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📡 Endpoints Disponibles

### **GET /** - Información de la API
```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "name": "Agromate API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "health": "/health",
    "news": "/api/news",
    "stats": "/api/stats",
    "recent": "/api/recent",
    "pipeline": "/api/pipeline/run"
  }
}
```

---

### **GET /health** - Health Check
Verifica el estado del servicio y la conexión a la base de datos.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-31T21:16:00Z",
  "database": "connected"
}
```

---

### **GET /api/news** - Lista de Noticias
Obtiene una lista de noticias con análisis de sentimiento.

**Parámetros:**
- `limit` (opcional): Máximo de artículos (default: 50, max: 200)
- `sentiment` (opcional): Filtrar por sentimiento (ALCISTA/BAJISTA/NEUTRAL)

**PowerShell:**
```powershell
# Obtener 10 noticias
Invoke-WebRequest -Uri 'http://localhost:8000/api/news?limit=10' -UseBasicParsing | Select-Object -ExpandProperty Content

# Filtrar solo noticias ALCISTAS
Invoke-WebRequest -Uri 'http://localhost:8000/api/news?sentiment=ALCISTA' -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Respuesta:**
```json
{
  "total": 3,
  "articles": [
    {
      "id": "6d82b9f5-948f-4c4e-9e50-ebb3868ea84b",
      "title": "Un vino entre caldenes: En General Acha, Horacio Marín contó...",
      "source": "Bichos de Campo",
      "url": "https://bichosdecampo.com/un-vino-entre-caldenes",
      "published_at": "2026-01-31T15:21:00Z",
      "sentiment": "NEUTRAL",
      "confidence": 0.82,
      "commodity": "SOJA",
      "created_at": "2026-01-31T21:04:30Z",
      "updated_at": "2026-01-31T21:04:30Z"
    }
  ]
}
```

---

### **GET /api/news/{id}** - Noticia por ID
Obtiene una noticia específica por su UUID.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri 'http://localhost:8000/api/news/6d82b9f5-948f-4c4e-9e50-ebb3868ea84b' -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

### **GET /api/stats** - Estadísticas de Sentimiento
Obtiene estadísticas agregadas de todos los artículos.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri 'http://localhost:8000/api/stats' -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Respuesta:**
```json
{
  "total": 9,
  "alcista": 6,
  "bajista": 3,
  "neutral": 0,
  "null": 0,
  "alcista_percentage": 66.7,
  "bajista_percentage": 33.3,
  "neutral_percentage": 0.0
}
```

---

### **GET /api/recent** - Noticias Recientes
Obtiene noticias de las últimas N horas.

**Parámetros:**
- `hours` (opcional): Horas hacia atrás (default: 24, max: 168)

**PowerShell:**
```powershell
# Últimas 24 horas
Invoke-WebRequest -Uri 'http://localhost:8000/api/recent' -UseBasicParsing | Select-Object -ExpandProperty Content

# Últimas 48 horas
Invoke-WebRequest -Uri 'http://localhost:8000/api/recent?hours=48' -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

### **POST /api/pipeline/run** - Ejecutar Pipeline
Ejecuta el pipeline completo (Scraping → Análisis → Base de datos) en segundo plano.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri 'http://localhost:8000/api/pipeline/run' -Method POST -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Respuesta:**
```json
{
  "status": "running",
  "message": "Pipeline started in background. Check /api/stats for updates."
}
```

**Nota:** El pipeline corre en background. Consultá `/api/stats` después de unos segundos para ver los nuevos datos.

---

## 🌐 CORS

CORS está configurado para permitir todas las origins (`*`). Esto es ideal para desarrollo, pero en producción deberías especificar origins exactos:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.com"],  # En producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Documentación Interactiva

### Swagger UI
Abrí en tu navegador: http://localhost:8000/docs

Características:
- ✅ Probar todos los endpoints interactivamente
- ✅ Ver esquemas de request/response
- ✅ Ejecutar llamadas directamente desde el navegador

### ReDoc
Abrí en tu navegador: http://localhost:8000/redoc

Documentación alternativa más legible.

---

## 🧪 Testing con el Navegador

También podés probar directamente en el navegador:

- **Health:** http://localhost:8000/health
- **Noticias:** http://localhost:8000/api/news?limit=5
- **Stats:** http://localhost:8000/api/stats
- **Recent:** http://localhost:8000/api/recent?hours=24

---

## 🔧 Desarrollo

### Hot Reload
El servidor está configurado con `reload=True`, así que los cambios en el código se reflejan automáticamente.

### Logs
Los logs se muestran en la consola donde ejecutaste `run_server.py`.

### Detener el servidor
Presioná `Ctrl+C` en la terminal donde corre el servidor.

---

## 📊 Esquemas de Datos

### NewsResponse
```typescript
{
  id: string;              // UUID
  title: string;
  source: string;
  url: string;
  published_at: string | null;  // ISO 8601
  sentiment: "ALCISTA" | "BAJISTA" | "NEUTRAL" | null;
  confidence: number | null;     // 0.00 - 1.00
  commodity: string;             // default: "SOJA"
  created_at: string;            // ISO 8601
  updated_at: string;            // ISO 8601
}
```

### SentimentStats
```typescript
{
  total: number;
  alcista: number;
  bajista: number;
  neutral: number;
  null: number;
  alcista_percentage: number;
  bajista_percentage: number;
  neutral_percentage: number;
}
```

---

## ✨ Próximos Pasos

Con la API funcionando, ahora podés:

1. **Frontend (Fase 6):** Crear el dashboard Next.js
2. **Integración:** Conectar el frontend a estos endpoints
3. **Deploy:** Subir a producción (Vercel + Railway/Render)

---

## 🎯 Estado Actual

| Componente | Status |
|------------|--------|
| Scraping RSS | ✅ 3 fuentes activas |
| Análisis de Sentimiento | ✅ Mock LLM |
| Base de Datos | ✅ Supabase conectado |
| API REST | ✅ 7 endpoints funcionales |
| CORS | ✅ Configurado |
| Docs | ✅ Swagger + ReDoc |

---

**¡La API de Agromate está lista para consumir desde el frontend!** 🚀
