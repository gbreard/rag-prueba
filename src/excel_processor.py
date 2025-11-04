"""
Procesador de archivos Excel para datos de empleo
"""
import pandas as pd
from typing import Dict, List, Any
import json


class ExcelProcessor:
    """Procesa archivos Excel y extrae datos estructurados de empleo"""

    def __init__(self):
        self.df = None
        self.columns = []
        self.text_columns = []
        self.numeric_columns = []

    def load_excel(self, file_path: str) -> Dict[str, Any]:
        """
        Carga un archivo Excel y detecta automáticamente las columnas

        Args:
            file_path: Ruta al archivo Excel

        Returns:
            Dict con información del archivo cargado
        """
        try:
            # Leer Excel
            self.df = pd.read_excel(file_path)

            # Limpiar nombres de columnas
            self.df.columns = self.df.columns.str.strip()

            # Detectar tipos de columnas
            self.columns = list(self.df.columns)
            self._detect_column_types()

            # Limpiar datos
            self._clean_data()

            return {
                "success": True,
                "num_rows": len(self.df),
                "columns": self.columns,
                "text_columns": self.text_columns,
                "numeric_columns": self.numeric_columns,
                "sample": self.df.head(3).to_dict(orient='records')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _detect_column_types(self):
        """Detecta automáticamente qué columnas son texto y cuáles son numéricas"""
        for col in self.columns:
            dtype = self.df[col].dtype

            if dtype in ['object', 'string']:
                self.text_columns.append(col)
            elif dtype in ['int64', 'float64', 'int32', 'float32']:
                self.numeric_columns.append(col)
            else:
                # Por defecto, tratar como texto
                self.text_columns.append(col)

    def _clean_data(self):
        """Limpia y normaliza los datos"""
        # Rellenar valores nulos
        for col in self.text_columns:
            self.df[col] = self.df[col].fillna('')

        for col in self.numeric_columns:
            self.df[col] = self.df[col].fillna(0)

        # Convertir todo a string para columnas de texto
        for col in self.text_columns:
            self.df[col] = self.df[col].astype(str)

    def get_documents(self) -> List[Dict[str, Any]]:
        """
        Convierte el DataFrame en una lista de documentos para el vector store

        Returns:
            Lista de documentos con texto y metadata
        """
        documents = []

        for idx, row in self.df.iterrows():
            # Crear texto combinado para búsqueda semántica
            text_parts = []
            for col in self.text_columns:
                value = row[col]
                if value and str(value).strip():
                    text_parts.append(f"{col}: {value}")

            combined_text = "\n".join(text_parts)

            # Metadata estructurada
            metadata = {
                "row_id": int(idx),
                **{col: row[col] for col in self.columns}
            }

            documents.append({
                "id": f"doc_{idx}",
                "text": combined_text,
                "metadata": metadata
            })

        return documents

    def get_dataframe(self) -> pd.DataFrame:
        """Retorna el DataFrame procesado"""
        return self.df

    def search_structured(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Búsqueda estructurada usando filtros

        Args:
            filters: Diccionario con filtros a aplicar

        Returns:
            DataFrame filtrado
        """
        df_filtered = self.df.copy()

        for column, condition in filters.items():
            if column not in self.columns:
                continue

            if isinstance(condition, dict):
                # Filtros complejos: {"operator": ">=", "value": 50000}
                operator = condition.get("operator", "==")
                value = condition.get("value")

                if operator == ">=":
                    df_filtered = df_filtered[df_filtered[column] >= value]
                elif operator == "<=":
                    df_filtered = df_filtered[df_filtered[column] <= value]
                elif operator == ">":
                    df_filtered = df_filtered[df_filtered[column] > value]
                elif operator == "<":
                    df_filtered = df_filtered[df_filtered[column] < value]
                elif operator == "==":
                    df_filtered = df_filtered[df_filtered[column] == value]
                elif operator == "contains":
                    df_filtered = df_filtered[df_filtered[column].str.contains(str(value), case=False, na=False)]
            else:
                # Filtro simple: igualdad
                df_filtered = df_filtered[df_filtered[column] == condition]

        return df_filtered
