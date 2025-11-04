# 🔀 Mergear a Main para Deployment

Antes de deployar en Streamlit Cloud, necesitas mergear esta rama a `main`:

## Opción 1: Via GitHub (Recomendada)

1. Ve a tu repositorio en GitHub: https://github.com/gbreard/rag-prueba

2. Verás un banner que dice "Compare & pull request" para la rama `claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE`

3. Haz clic en **"Compare & pull request"**

4. Revisa los cambios

5. Haz clic en **"Create pull request"**

6. Luego **"Merge pull request"**

7. **"Confirm merge"**

## Opción 2: Via Git Local

```bash
# 1. Asegúrate de estar en la rama actual
git checkout claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE

# 2. Cambia a main
git checkout main

# 3. Merge de la rama
git merge claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE

# 4. Push a main
git push origin main
```

## Opción 3: Deployar directamente desde la rama

También puedes deployar directamente desde la rama `claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE` sin hacer merge a main:

1. En Streamlit Cloud, al crear la app
2. Selecciona **Branch:** `claude/design-rag-system-011CUoSc6SBtVMZTvvEN3ZLE`
3. Mantén el resto igual

---

Una vez hecho el merge (o si usas opción 3), continúa con **DEPLOY.md** para deployar en Streamlit Cloud.
