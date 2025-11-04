"""
Sistema de embeddings usando sentence-transformers
"""
from sentence_transformers import SentenceTransformer
from typing import List
import os


class EmbeddingModel:
    """Modelo de embeddings local y gratuito"""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Inicializa el modelo de embeddings

        Args:
            model_name: Nombre del modelo de sentence-transformers
                       Por defecto usa modelo multilingüe (español/inglés)
        """
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Carga el modelo de embeddings"""
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise Exception(f"Error cargando modelo de embeddings: {str(e)}")

    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings para una lista de textos

        Args:
            texts: Lista de textos a codificar

        Returns:
            Lista de embeddings (vectores)
        """
        if not texts:
            return []

        # Generar embeddings
        embeddings = self.model.encode(texts, show_progress_bar=False)

        return embeddings.tolist()

    def encode_single(self, text: str) -> List[float]:
        """
        Genera embedding para un solo texto

        Args:
            text: Texto a codificar

        Returns:
            Embedding (vector)
        """
        embedding = self.model.encode([text], show_progress_bar=False)
        return embedding[0].tolist()

    def get_dimension(self) -> int:
        """Retorna la dimensión del vector de embeddings"""
        return self.model.get_sentence_embedding_dimension()
