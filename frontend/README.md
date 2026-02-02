# Agromate Frontend

Dashboard de Next.js para Agromate - Análisis de sentimiento del mercado agropecuario argentino.

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Asegurate de que el backend esté corriendo

El frontend necesita que la API esté activa en `http://localhost:8000`:

```bash
cd ../backend
.\venv\Scripts\python run_server.py
```

### 3. Levantar el servidor de desarrollo

```bash
cd frontend
npm run dev
```

El dashboard estará disponible en: **http://localhost:3000**

---

## 📁 Estructura de Archivos

```
frontend/src/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Página principal (Dashboard)
│   └── globals.css         # Estilos globales + Tailwind
│
├── components/
│   ├── Dashboard.tsx       # Componente principal con lógica
│   ├── NewsCard.tsx        # Card de noticia individual
│   └── SentimentBadge.tsx  # Badge de sentimiento (verde/rojo/gris)
│
├── lib/
│   └── api.ts              # Cliente API (fetch)
│
└── types/
    └── index.ts            # Definiciones TypeScript
```

---

## 🎨 Características del Dashboard

### **Vista de Estadísticas**
- 4 cards con métricas clave:
  - Total de noticias
  - Noticias alcistas (verde)
  - Noticias bajistas (rojo)
  - Noticias neutrales (gris)

### **Grid de Noticias**
- Muestra las últimas 20 noticias analizadas
- Cada card incluye:
  - Título con link externo
  - Fuente y fecha de publicación
  - Badge de sentimiento con % de confianza
  - Commodity relacionado

### **Botón de Actualización**
- Ejecuta el pipeline completo (scraping + análisis)
- Muestra estado de "Cargando..."
- Actualiza automáticamente después de 3 segundos

---

## 🔌 Conexión con la API

El frontend consume estos endpoints:

- `GET /api/news?limit=20` - Lista de noticias
- `GET /api/stats` - Estadísticas de sentimiento
- `POST /api/pipeline/run` - Ejecutar pipeline

Configurá la URL base en `src/lib/api.ts` si tu backend corre en otro puerto.

---

## 🎨 Personalización

### Colores de Sentimiento

Editá `src/components/SentimentBadge.tsx` para cambiar los colores:

```tsx
case 'ALCISTA':
  return {
    bg: 'bg-green-100',  // Fondo verde claro
    text: 'text-green-800',  // Texto verde oscuro
    icon: '↑',
    label: 'Alcista'
  };
```

### Límite de Noticias

Editá `src/components/Dashboard.tsx` línea 27:

```tsx
fetchNews(20)  // Cambiá 20 por el número que quieras
```

---

## 🏗️ Build para Producción

```bash
npm run build
npm start
```

Esto generará una build optimizada en `.next/`.

---

## 🐛 Troubleshooting

### Error: "Failed to fetch"
- ✅ Verificá que el backend esté corriendo en puerto 8000
- ✅ Revisá la consola del navegador para detalles

### CORS Error
- ✅ Asegurate que el backend tenga CORS configurado (ya está en `main.py`)

### Estilos no se aplican
- ✅ Verificá que Tailwind esté configurado correctamente
- ✅ Reiniciá el servidor de desarrollo

---

## 📊 Próximos Pasos

- [ ] Agregar gráficos (Chart.js o Recharts)
- [ ] Filtros por fuente y fecha
- [ ] Paginación de noticias
- [ ] Dark mode
- [ ] Deploy en Vercel

---

**El frontend de Agromate está listo para visualizar análisis de mercado en tiempo real!** 🚀
