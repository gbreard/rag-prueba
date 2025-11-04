# 🚀 Guía de Deployment en Streamlit Cloud

Esta guía te ayudará a deployar el sistema RAG en Streamlit Cloud **GRATIS** y hacerlo accesible públicamente en internet.

## ⏱️ Tiempo estimado: 10 minutos

---

## 📋 Pre-requisitos

- ✅ Cuenta de GitHub (donde ya está el código)
- ✅ API Key de Groq (obtén una gratis en: https://console.groq.com/keys)
- ✅ Cuenta de email para Streamlit Cloud

---

## 🎯 Paso a Paso

### 1️⃣ Crear cuenta en Streamlit Cloud

1. Ve a: **https://share.streamlit.io/**
2. Haz clic en **"Sign up"**
3. Selecciona **"Continue with GitHub"**
4. Autoriza a Streamlit Cloud para acceder a tus repositorios

### 2️⃣ Preparar el repositorio (Ya está listo ✅)

El código ya está pusheado a GitHub en la rama:
```
claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE
```

**IMPORTANTE:** Antes de deployar, deberías hacer merge de esta rama a `main` o la rama principal de tu repo.

### 3️⃣ Crear nueva app en Streamlit Cloud

1. En Streamlit Cloud dashboard, haz clic en **"New app"**

2. Selecciona:
   - **Repository:** `gbreard/rag-prueba`
   - **Branch:** `main` (o la rama donde hiciste merge)
   - **Main file path:** `app.py`

3. Haz clic en **"Advanced settings"** antes de deployar

### 4️⃣ Configurar Secrets (IMPORTANTE)

En la sección **"Secrets"**, pega esto (reemplaza `tu_api_key_aqui` con tu API key real de Groq):

```toml
GROQ_API_KEY = "tu_api_key_aqui"
GROQ_MODEL = "llama-3.1-70b-versatile"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
```

⚠️ **IMPORTANTE:**
- Reemplaza `tu_api_key_aqui` con tu API key real de Groq
- No compartas esta configuración públicamente
- Streamlit Cloud encripta y protege tus secrets

### 5️⃣ Deploy

1. Haz clic en **"Deploy"**
2. Espera 3-5 minutos mientras se instalan las dependencias
3. Verás el progreso en tiempo real

### 6️⃣ ¡Listo! 🎉

Una vez completado, tu app estará disponible en:
```
https://[nombre-app].streamlit.app
```

Por ejemplo: `https://rag-empleo.streamlit.app`

---

## 🔧 Configuración Adicional (Opcional)

### Cambiar nombre de la app

1. En el dashboard, haz clic en **"⚙️ Settings"**
2. Ve a **"General"**
3. Cambia el **App name**
4. Guarda cambios

### Hacer la app privada

1. En **"Settings"**
2. Ve a **"Sharing"**
3. Selecciona **"Private"**
4. Agrega emails de personas autorizadas

### Actualizar secrets

1. En **"Settings"**
2. Ve a **"Secrets"**
3. Edita el contenido
4. Guarda cambios (la app se reiniciará automáticamente)

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real

1. En el dashboard, haz clic en tu app
2. Haz clic en **"Manage app"**
3. Ve a **"Logs"**

### Reiniciar la app

Si hay algún problema:
1. **Settings → Reboot app**
2. Espera 1-2 minutos

---

## 🔄 Actualizar la App

Cada vez que hagas push al repositorio:
1. Streamlit Cloud detecta cambios automáticamente
2. Re-deploya la app
3. Tus usuarios ven la nueva versión

Si no se actualiza automáticamente:
- **Settings → Reboot app**

---

## 💾 Limitaciones de Streamlit Cloud (Tier Gratuito)

| Recurso | Límite |
|---------|--------|
| CPU | 1 vCPU |
| RAM | 1 GB |
| Storage | Sin límite de archivos (temporales) |
| Uptime | 24/7 (pero puede "dormir" si no hay uso) |
| Apps | 3 apps públicas, 1 privada |
| Uploads | 200 MB por archivo |

**Nota:** Para archivos Excel muy grandes (>100MB), considera usar la versión local.

---

## ⚠️ Troubleshooting

### Error: "Module not found"

**Solución:** Verifica que `requirements.txt` tenga todas las dependencias.

```bash
# En local, verifica que funcione:
pip install -r requirements.txt
streamlit run app.py
```

### Error: "App is using too much memory"

**Causa:** Archivo Excel muy grande.

**Solución:**
1. Reduce el tamaño del Excel
2. O usa la app localmente

### Error: "GROQ_API_KEY not found"

**Solución:**
1. Ve a **Settings → Secrets**
2. Verifica que `GROQ_API_KEY` esté configurada correctamente
3. No debe tener espacios extra ni comillas dobles incorrectas

### La app está muy lenta

**Causas posibles:**
- Primera carga siempre es lenta (descarga modelos de embeddings)
- Archivo Excel muy grande
- Muchos usuarios simultáneos

**Soluciones:**
- Espera a que cargue la primera vez (luego será más rápido)
- Reduce tamaño del Excel
- Considera upgrade a plan pagado ($20/mes) para más recursos

---

## 🔐 Seguridad

### ¿Es seguro mi API key?

✅ **SÍ:** Streamlit Cloud encripta todos los secrets. No son visibles ni siquiera en los logs.

### ¿Mis datos están seguros?

✅ Los archivos Excel se procesan en memoria y se eliminan cuando cierras la sesión
✅ ChromaDB se almacena temporalmente (se borra al reiniciar app)
⚠️ Para datos super sensibles, usa la versión local

### ¿Quién puede acceder?

Por defecto: **Cualquiera con el link**

Para hacerla privada:
1. **Settings → Sharing → Private**
2. Agrega emails autorizados

---

## 📈 Métricas y Analytics

Streamlit Cloud incluye analytics básicas:
1. **Settings → Analytics**
2. Verás:
   - Número de visitantes
   - Tiempo de uso
   - Errores

---

## 🎓 Recursos Adicionales

- **Documentación oficial:** https://docs.streamlit.io/streamlit-community-cloud
- **Foro de soporte:** https://discuss.streamlit.io/
- **Status de servicios:** https://streamlitstatus.com/

---

## 🆘 ¿Necesitas ayuda?

Si tienes problemas:
1. Revisa los **logs** en Streamlit Cloud
2. Verifica que funcione en **local** primero
3. Consulta la documentación oficial
4. Abre un issue en el repositorio

---

## ✅ Checklist de Deployment

Antes de deployar, verifica:

- [ ] Código pusheado a GitHub
- [ ] `requirements.txt` completo
- [ ] API key de Groq lista
- [ ] Cuenta de Streamlit Cloud creada
- [ ] Secrets configuradas correctamente
- [ ] App probada localmente

---

**¡Listo para deployar! 🚀**

Una vez deployado, comparte el link con quien quieras: colegas, clientes, amigos, etc.
