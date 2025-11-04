# 🚀 Guía de Inicio Rápido

## Pasos para empezar en 5 minutos

### 1️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key de Groq

**Obtener API key (GRATIS):**
1. Ve a https://console.groq.com/keys
2. Crea una cuenta
3. Genera una API key

**Configurar:**
```bash
cp .env.example .env
```

Edita `.env` y añade tu key:
```env
GROQ_API_KEY=gsk_tu_api_key_aqui
```

### 3️⃣ Crear datos de ejemplo (opcional)

```bash
python create_sample_data.py
```

Esto creará `ejemplos/empleos_ejemplo.xlsx` con 15 ofertas de trabajo de prueba.

### 4️⃣ Iniciar la aplicación

```bash
streamlit run app.py
```

### 5️⃣ Usar el sistema

1. La app se abrirá en http://localhost:8501
2. Sube tu Excel (o usa el de ejemplo en `ejemplos/empleos_ejemplo.xlsx`)
3. Haz clic en "Procesar Archivo"
4. ¡Comienza a hacer preguntas!

## Ejemplos de preguntas

```
¿Cuáles son los trabajos mejor pagados?
Encuentra trabajos remotos
¿Qué empresas están en Madrid?
Muéstrame empleos que requieran Python
¿Cuál es el salario promedio?
Dame trabajos con más de 5 años de experiencia
```

## ¿Problemas?

### Error: GROQ_API_KEY no encontrada
- Verifica que el archivo `.env` existe
- Asegúrate de que tiene `GROQ_API_KEY=tu_key`
- Reinicia la aplicación

### Error al instalar dependencias
```bash
# Actualiza pip primero
pip install --upgrade pip
pip install -r requirements.txt
```

### La primera consulta es lenta
- Es normal, está cargando los modelos
- Las siguientes serán más rápidas

## Estructura del Excel

Tu Excel puede tener cualquier estructura, pero funciona mejor con:

- **Columnas de texto**: Título, Empresa, Descripción, Habilidades, etc.
- **Columnas numéricas**: Salario, Experiencia (años), etc.
- **Primera fila**: Nombres de columnas
- **Resto**: Datos

## Próximos pasos

- Lee el [README.md](README.md) completo para más detalles
- Prueba con tus propios datos de empleo
- Ajusta la configuración en la barra lateral
- Experimenta con diferentes tipos de preguntas

---

**¡Listo para empezar! 🎉**
