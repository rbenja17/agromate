# 🚀 Deploy Guide - Agromate

Este documento explica cómo deployar Agromate a producción con **costo $0**.

## Arquitectura de Producción

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Cloudflare Pages   │────▶│   Render (Free)     │────▶│  Supabase (Free)    │
│  (Frontend React)   │     │   (FastAPI Backend) │     │  (PostgreSQL)       │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                      │
                                      ▼
                            ┌─────────────────────┐
                            │  Google Gemini API  │
                            │     (Free Tier)     │
                            └─────────────────────┘
```

---

## 1️⃣ Deploy Backend → Render

### Paso 1: Crear cuenta en Render
1. Ir a https://render.com
2. Sign up con GitHub

### Paso 2: Crear Web Service
1. Click **"New +"** → **"Web Service"**
2. Conectar tu repositorio de GitHub
3. Configurar:
   - **Name:** `agromate-api`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Paso 3: Variables de Entorno
En Render Dashboard → Environment, agregar:

| Variable | Valor |
|----------|-------|
| `SUPABASE_URL` | `https://tu-proyecto.supabase.co` |
| `SUPABASE_ANON_KEY` | `tu-anon-key` |
| `GOOGLE_API_KEY` | `tu-gemini-api-key` |
| `ENVIRONMENT` | `production` |

### Paso 4: Deploy
Click **"Create Web Service"** - el deploy es automático.

Tu API estará en: `https://agromate-api.onrender.com`

### ⚠️ Nota sobre Cold Starts
El free tier de Render tiene cold starts de ~30 segundos si la app no se usa por 15 minutos.
- **Solución:** Configurar [UptimeRobot](https://uptimerobot.com) para hacer ping a `/health` cada 14 minutos.

---

## 2️⃣ Deploy Frontend → Cloudflare Pages

### Paso 1: Crear cuenta en Cloudflare
1. Ir a https://dash.cloudflare.com
2. Sign up (gratis)

### Paso 2: Crear Pages Project
1. En sidebar: **Workers & Pages** → **Create application** → **Pages**
2. **Connect to Git** → Autorizar GitHub
3. Seleccionar tu repositorio

### Paso 3: Configurar Build
- **Project name:** `agromate`
- **Production branch:** `main`
- **Framework preset:** Next.js (Static HTML Export)
- **Root directory:** `frontend`
- **Build command:** `npm run build`
- **Build output directory:** `out`

### Paso 4: Variables de Entorno
En Settings → Environment Variables, agregar:

| Variable | Valor |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://agromate-api.onrender.com` |

⚠️ **Importante:** Reemplazar con la URL real de tu backend en Render.

### Paso 5: Deploy
Click **"Save and Deploy"**

Tu frontend estará en: `https://agromate.pages.dev`

---

## 3️⃣ Configurar UptimeRobot (Evitar Cold Starts)

1. Ir a https://uptimerobot.com (crear cuenta gratis)
2. **Add New Monitor:**
   - Type: HTTP(s)
   - URL: `https://agromate-api.onrender.com/health`
   - Monitoring Interval: 5 minutes
3. Esto mantiene la app "caliente" y evita cold starts.

---

## 4️⃣ Post-Deploy Checklist

- [ ] Backend responde en `/health`
- [ ] Frontend carga correctamente
- [ ] Dashboard muestra datos de Supabase
- [ ] Filtros funcionan
- [ ] Gráficos se actualizan
- [ ] Pipeline de scraping funciona

---

## 🔧 Troubleshooting

### CORS Error
Si ves errores de CORS, verificar que:
1. La URL del frontend está en `ALLOWED_ORIGINS` en `backend/main.py`
2. Variables de entorno están correctas

### API no responde
1. Verificar logs en Render Dashboard
2. Verificar que las variables de entorno están configuradas
3. Probar `/health` endpoint directamente

### Build fails en Cloudflare
1. Verificar que `next.config.mjs` tiene `output: 'export'`
2. Verificar que `NEXT_PUBLIC_API_URL` está configurada

---

## 💰 Costos

| Servicio | Plan | Costo |
|----------|------|-------|
| Render | Free | $0 |
| Cloudflare Pages | Free | $0 |
| Supabase | Free | $0 |
| Google Gemini | Free Tier (15 RPM) | $0 |
| **Total** | | **$0/mes** |

---

## 🔗 URLs de Producción

Una vez deployado:
- **Frontend:** https://agromate.pages.dev
- **Backend API:** https://agromate-api.onrender.com
- **API Docs:** https://agromate-api.onrender.com/docs
