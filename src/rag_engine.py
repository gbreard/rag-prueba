"""
Motor RAG principal que coordina todos los componentes
"""
from typing import Dict, Any, List, Optional
import pandas as pd

from .excel_processor import ExcelProcessor
from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .llm_client import GroqClient


class RAGEngine:
    """Motor RAG para consultas sobre datos de empleo"""

    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        groq_model: str = "llama-3.1-70b-versatile",
        embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    ):
        """
        Inicializa el motor RAG

        Args:
            groq_api_key: API key de Groq
            groq_model: Modelo de Groq a usar
            embedding_model: Modelo de embeddings a usar
        """
        self.excel_processor = ExcelProcessor()
        self.embedding_model = EmbeddingModel(model_name=embedding_model)
        self.vector_store = VectorStore()
        self.llm_client = GroqClient(api_key=groq_api_key, model=groq_model)

        self.is_loaded = False
        self.columns = []

    def load_excel(self, file_path: str) -> Dict[str, Any]:
        """
        Carga un archivo Excel y lo indexa en el vector store

        Args:
            file_path: Ruta al archivo Excel

        Returns:
            Dict con información del proceso
        """
        # 1. Cargar Excel
        result = self.excel_processor.load_excel(file_path)
        if not result["success"]:
            return result

        self.columns = result["columns"]

        # 2. Obtener documentos
        documents = self.excel_processor.get_documents()

        # 3. Generar embeddings
        texts = [doc["text"] for doc in documents]
        embeddings = self.embedding_model.encode(texts)

        # 4. Crear/resetear colección e indexar
        self.vector_store.create_collection(reset=True)
        self.vector_store.add_documents(documents, embeddings)

        self.is_loaded = True

        return {
            "success": True,
            "num_rows": result["num_rows"],
            "num_indexed": len(documents),
            "columns": self.columns,
            "sample": result["sample"]
        }

    def query(
        self,
        question: str,
        top_k: int = 5,
        use_filters: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa una consulta en lenguaje natural

        Args:
            question: Pregunta del usuario
            top_k: Número de resultados a recuperar
            use_filters: Si True, intenta extraer filtros de la pregunta

        Returns:
            Dict con la respuesta y resultados
        """
        if not self.is_loaded:
            return {
                "success": False,
                "error": "No hay datos cargados. Por favor sube un archivo Excel primero."
            }

        # 1. Extraer filtros si está habilitado
        filters = {}
        if use_filters:
            extracted = self.llm_client.extract_filters(question, self.columns)
            filters = extracted.get("filters", {})

        # 2. Generar embedding de la consulta
        query_embedding = self.embedding_model.encode_single(question)

        # 3. Búsqueda semántica en vector store
        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=top_k
        )

        # 4. Construir contexto para el LLM
        context = self._build_context(search_results)

        # 5. Generar respuesta con el LLM
        response = self.llm_client.generate_response(
            query=question,
            context=context
        )

        # 6. Preparar resultados estructurados
        results = []
        for i, metadata in enumerate(search_results["metadatas"]):
            results.append({
                "score": 1 - search_results["distances"][i],  # Convertir distancia a similitud
                "data": metadata
            })

        return {
            "success": True,
            "response": response,
            "results": results,
            "num_results": len(results),
            "filters_applied": filters
        }

    def _build_context(self, search_results: Dict[str, Any]) -> str:
        """
        Construye el contexto para el LLM a partir de los resultados

        Args:
            search_results: Resultados de la búsqueda vectorial

        Returns:
            Contexto formateado
        """
        context_parts = []

        for i, (doc, metadata) in enumerate(zip(
            search_results["documents"],
            search_results["metadatas"]
        ), 1):
            context_parts.append(f"--- Registro {i} ---")
            context_parts.append(doc)
            context_parts.append("")

        return "\n".join(context_parts)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas de los datos cargados

        Returns:
            Dict con estadísticas
        """
        if not self.is_loaded:
            return {"success": False, "error": "No hay datos cargados"}

        df = self.excel_processor.get_dataframe()

        stats = {
            "success": True,
            "total_records": len(df),
            "columns": self.columns,
            "text_columns": self.excel_processor.text_columns,
            "numeric_columns": self.excel_processor.numeric_columns
        }

        # Estadísticas de columnas numéricas
        numeric_stats = {}
        for col in self.excel_processor.numeric_columns:
            numeric_stats[col] = {
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "mean": float(df[col].mean()),
                "median": float(df[col].median())
            }

        stats["numeric_stats"] = numeric_stats

        return stats

    def get_sample_data(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene una muestra de los datos

        Args:
            n: Número de registros a retornar

        Returns:
            Lista de registros
        """
        if not self.is_loaded:
            return []

        df = self.excel_processor.get_dataframe()
        return df.head(n).to_dict(orient='records')
