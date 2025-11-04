# 💼 Sistema RAG para Datos de Empleo

Sistema de Retrieval-Augmented Generation (RAG) para interactuar con bases de conocimiento de empleo utilizando LLM gratuito (Groq).

## 🚀 Deploy Rápido

**¿Quieres deployar en internet?** Sigue la [Guía de Deployment en Streamlit Cloud](DEPLOY.md) - Es **GRATIS** y toma 10 minutos.

**¿Prefieres usarlo local?** Continúa leyendo esta guía.

## 🌟 Características

- **Interfaz web intuitiva** con Streamlit
- **Carga automática de Excel** - sube tu archivo y comienza a preguntar
- **Búsqueda semántica** usando embeddings multilingües (español/inglés)
- **LLM gratuito** con Groq (llama-3.1-70b)
- **Detección automática de columnas** - no necesitas configurar nada
- **Consultas en lenguaje natural** - pregunta como hablarías normalmente
- **Búsqueda híbrida** - combina filtros estructurados con búsqueda semántica

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Excel File     │
└────────┬────────┘
         │
┌────────▼────────┐
│ Excel Processor │ (pandas)
└────────┬────────┘
         │
┌────────▼────────┐
│   Embeddings    │ (sentence-transformers)
└────────┬────────┘
         │
┌────────▼────────┐
│  Vector Store   │ (ChromaDB)
└────────┬────────┘
         │
┌────────▼────────┐
│   RAG Engine    │
└────────┬────────┘
         │
┌────────▼────────┐
│   Groq LLM      │ (llama-3.1-70b)
└────────┬────────┘
         │
┌────────▼────────┐
│   Streamlit     │
└─────────────────┘
```

## 📋 Requisitos

- Python 3.8 o superior
- 4-8 GB RAM (para modelos de embeddings)
- Conexión a internet (para API de Groq)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd rag-prueba
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key de Groq
nano .env  # o usa tu editor preferido
```

**Obtener API key de Groq (GRATIS):**

1. Ve a https://console.groq.com/keys
2. Crea una cuenta (gratis)
3. Genera una API key
4. Cópiala en el archivo `.env`:

```env
GROQ_API_KEY=gsk_tu_api_key_aqui
```

## 🎯 Uso

### Iniciar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### Pasos para usar el sistema

1. **Sube tu archivo Excel** en la barra lateral
2. **Haz clic en "Procesar Archivo"** - el sistema detectará automáticamente las columnas
3. **Comienza a hacer preguntas** en lenguaje natural

### Ejemplos de preguntas

```
¿Cuáles son los trabajos mejor pagados?
Encuentra empleos remotos de desarrollo
¿Qué empresas están contratando desarrolladores Python?
Muéstrame trabajos en Madrid con salario mayor a 50000
¿Cuáles son las habilidades más demandadas?
Dame un resumen de los empleos disponibles
```

## 📊 Estructura del archivo Excel

El sistema acepta cualquier estructura de Excel, pero funciona mejor con columnas como:

| Título | Empresa | Ubicación | Salario | Descripción | Habilidades |
|--------|---------|-----------|---------|-------------|-------------|
| Desarrollador Python | Tech Corp | Madrid | 45000 | Desarrollo backend... | Python, Django, SQL |
| Data Scientist | AI Labs | Barcelona | 55000 | Análisis de datos... | Python, ML, TensorFlow |
| DevOps Engineer | Cloud Systems | Remoto | 50000 | Infraestructura cloud... | AWS, Docker, K8s |

**Nota:** El sistema detecta automáticamente las columnas, no necesitas usar nombres específicos.

## 🔧 Configuración avanzada

### Cambiar modelo de Groq

Edita el archivo `.env`:

```env
# Modelos disponibles:
# - llama-3.1-70b-versatile (recomendado, por defecto)
# - llama-3.1-8b-instant (más rápido, menos preciso)
# - mixtral-8x7b-32768 (alternativa)

GROQ_MODEL=llama-3.1-70b-versatile
```

### Cambiar modelo de embeddings

Edita el archivo `.env`:

```env
# Modelos disponibles:
# - paraphrase-multilingual-MiniLM-L12-v2 (por defecto, español/inglés)
# - paraphrase-MiniLM-L6-v2 (solo inglés, más rápido)
# - all-MiniLM-L6-v2 (solo inglés, más ligero)

EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

### Ajustar número de resultados

En la interfaz, usa el slider "Resultados a recuperar" (1-10)

## 📁 Estructura del proyecto

```
rag-prueba/
├── app.py                      # Interfaz Streamlit
├── requirements.txt            # Dependencias
├── .env.example               # Ejemplo de configuración
├── .gitignore                 # Archivos ignorados
├── README.md                  # Esta documentación
├── src/
│   ├── __init__.py
│   ├── excel_processor.py     # Procesamiento de Excel
│   ├── embeddings.py          # Sistema de embeddings
│   ├── vector_store.py        # Base de datos vectorial
│   ├── llm_client.py          # Cliente Groq
│   └── rag_engine.py          # Motor RAG principal
├── uploaded_files/            # Archivos Excel subidos
└── chroma_db/                 # Base de datos vectorial
```

## 🧪 Ejemplo de uso programático

Si quieres usar el sistema sin interfaz:

```python
from src.rag_engine import RAGEngine
import os

# Inicializar
engine = RAGEngine(groq_api_key=os.getenv("GROQ_API_KEY"))

# Cargar datos
result = engine.load_excel("datos_empleo.xlsx")
print(f"Cargados {result['num_rows']} registros")

# Hacer consultas
response = engine.query("¿Cuáles son los trabajos mejor pagados?")
print(response["response"])

# Ver resultados
for result in response["results"]:
    print(f"Similitud: {result['score']:.2%}")
    print(result["data"])
```

## 🐛 Solución de problemas

### Error: "GROQ_API_KEY no encontrada"

- Verifica que el archivo `.env` existe en la raíz del proyecto
- Asegúrate de que contiene `GROQ_API_KEY=tu_key`
- Reinicia la aplicación

### Error al cargar Excel

- Verifica que el archivo es `.xlsx` o `.xls`
- Asegúrate de que tiene al menos una fila de datos
- Prueba abrirlo primero en Excel/LibreOffice para verificar formato

### Respuestas lentas

- Primera consulta siempre es más lenta (carga modelos)
- Considera usar un modelo más rápido: `llama-3.1-8b-instant`
- Reduce el número de resultados en configuración

### Error: "Out of memory"

- Reduce el tamaño del archivo Excel
- Usa un modelo de embeddings más pequeño
- Cierra otras aplicaciones

## 🔐 Privacidad y seguridad

- **Embeddings locales**: Los embeddings se generan localmente en tu máquina
- **Datos locales**: Tu Excel se procesa y almacena solo en tu computadora
- **API Groq**: Solo se envía el contexto relevante (no todo el archivo) a Groq
- **Sin almacenamiento externo**: Nada se guarda en servidores externos

## 📈 Mejoras futuras

- [ ] Soporte para CSV y JSON
- [ ] Filtros avanzados en la interfaz
- [ ] Exportar resultados
- [ ] Gráficos y visualizaciones
- [ ] Modo offline con Ollama
- [ ] Múltiples archivos simultáneos
- [ ] Caché de consultas

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 💡 Créditos

- **LLM**: Groq (llama-3.1-70b)
- **Embeddings**: sentence-transformers
- **Vector Store**: ChromaDB
- **UI**: Streamlit
- **Data Processing**: pandas

## 📧 Contacto

¿Preguntas o sugerencias? Abre un issue en GitHub.

---

**¡Disfruta consultando tus datos de empleo! 🚀**
