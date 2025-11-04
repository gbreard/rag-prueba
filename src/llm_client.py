"""
Cliente para Groq LLM
"""
from groq import Groq
from typing import List, Dict, Any, Optional
import os


class GroqClient:
    """Cliente para interactuar con Groq API"""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-70b-versatile"):
        """
        Inicializa el cliente de Groq

        Args:
            api_key: API key de Groq (si no se provee, se busca en env)
            model: Modelo a usar
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no encontrada. Configúrala en el archivo .env")

        self.model = model
        self.client = Groq(api_key=self.api_key)

    def generate_response(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Genera una respuesta usando Groq

        Args:
            query: Pregunta del usuario
            context: Contexto recuperado (documentos relevantes)
            system_prompt: Prompt del sistema (opcional)
            temperature: Temperatura para la generación
            max_tokens: Máximo de tokens a generar

        Returns:
            Respuesta generada
        """
        if not system_prompt:
            system_prompt = """Eres un asistente experto en análisis de datos de empleo.
Tu tarea es responder preguntas sobre ofertas de trabajo usando la información proporcionada.

Instrucciones:
1. Responde SOLO basándote en la información del contexto
2. Si la información no está en el contexto, di "No tengo información sobre eso"
3. Sé específico y preciso en tus respuestas
4. Si hay múltiples resultados, organízalos de forma clara
5. Usa formato markdown para mejor legibilidad
6. Incluye números y estadísticas cuando sea relevante"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Contexto con información de empleos:
{context}

Pregunta del usuario: {query}

Responde la pregunta usando la información del contexto."""}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"

    def extract_filters(self, query: str, columns: List[str]) -> Dict[str, Any]:
        """
        Extrae filtros estructurados de una consulta en lenguaje natural

        Args:
            query: Consulta del usuario
            columns: Columnas disponibles en los datos

        Returns:
            Diccionario con filtros extraídos
        """
        system_prompt = f"""Eres un asistente que extrae filtros estructurados de consultas en lenguaje natural.

Columnas disponibles: {', '.join(columns)}

Extrae filtros de la consulta del usuario y devuélvelos en formato JSON.

Formato de respuesta:
{{
  "filters": {{
    "nombre_columna": "valor" o {{"operator": ">=", "value": valor}}
  }},
  "search_terms": ["término1", "término2"]
}}

Operadores válidos: ==, >=, <=, >, <, contains

Si no hay filtros específicos, devuelve {{"filters": {{}}, "search_terms": []}}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )

            # Parsear JSON de la respuesta
            import json
            content = response.choices[0].message.content

            # Extraer JSON si está en un bloque de código
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)
            return result

        except Exception as e:
            # Si falla, retornar vacío
            return {"filters": {}, "search_terms": []}
