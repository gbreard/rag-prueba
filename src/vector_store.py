"""
Vector Store usando ChromaDB
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import json


class VectorStore:
    """Almacenamiento vectorial con ChromaDB"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Inicializa el vector store

        Args:
            persist_directory: Directorio donde se persiste la base de datos
        """
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente de ChromaDB"""
        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        ))

    def create_collection(self, name: str = "employment_data", reset: bool = False):
        """
        Crea o carga una colección

        Args:
            name: Nombre de la colección
            reset: Si True, elimina la colección existente y crea una nueva
        """
        if reset:
            try:
                self.client.delete_collection(name)
            except:
                pass

        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ):
        """
        Añade documentos a la colección

        Args:
            documents: Lista de documentos con 'id', 'text' y 'metadata'
            embeddings: Lista de embeddings correspondientes
        """
        if not self.collection:
            raise Exception("Collection not initialized. Call create_collection first.")

        # Preparar datos
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = []

        for doc in documents:
            # ChromaDB requiere que metadata sea dict de strings
            metadata = {}
            for key, value in doc["metadata"].items():
                if isinstance(value, (int, float)):
                    metadata[key] = str(value)
                elif isinstance(value, str):
                    metadata[key] = value
                else:
                    metadata[key] = str(value)
            metadatas.append(metadata)

        # Añadir a la colección
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Búsqueda semántica en la colección

        Args:
            query_embedding: Embedding de la consulta
            n_results: Número de resultados a retornar
            where: Filtros de metadata (opcional)

        Returns:
            Resultados de la búsqueda
        """
        if not self.collection:
            raise Exception("Collection not initialized. Call create_collection first.")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }

    def get_count(self) -> int:
        """Retorna el número de documentos en la colección"""
        if not self.collection:
            return 0
        return self.collection.count()

    def delete_collection(self, name: str = "employment_data"):
        """Elimina una colección"""
        try:
            self.client.delete_collection(name)
        except:
            pass
