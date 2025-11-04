"""
Interfaz web con Streamlit para el sistema RAG de datos de empleo
"""
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

from src.rag_engine import RAGEngine

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="RAG Sistema de Empleo",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .result-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'rag_engine' not in st.session_state:
        try:
            api_key = os.getenv("GROQ_API_KEY")
            model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            embedding_model = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

            st.session_state.rag_engine = RAGEngine(
                groq_api_key=api_key,
                groq_model=model,
                embedding_model=embedding_model
            )
        except Exception as e:
            st.error(f"Error inicializando el sistema: {str(e)}")
            st.session_state.rag_engine = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def sidebar():
    """Barra lateral con configuración y carga de archivos"""
    st.sidebar.markdown("## 📁 Cargar Datos")

    uploaded_file = st.sidebar.file_uploader(
        "Sube tu archivo Excel",
        type=['xlsx', 'xls'],
        help="Sube un archivo Excel con datos de empleo"
    )

    if uploaded_file is not None:
        if st.sidebar.button("🚀 Procesar Archivo", type="primary"):
            with st.spinner("Procesando archivo..."):
                # Guardar archivo temporalmente
                upload_dir = Path("uploaded_files")
                upload_dir.mkdir(exist_ok=True)
                file_path = upload_dir / uploaded_file.name

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Cargar en el RAG
                result = st.session_state.rag_engine.load_excel(str(file_path))

                if result["success"]:
                    st.session_state.data_loaded = True
                    st.sidebar.success(f"✅ Archivo procesado correctamente!")
                    st.sidebar.info(f"📊 {result['num_rows']} registros indexados")

                    # Mostrar columnas detectadas
                    with st.sidebar.expander("📋 Columnas detectadas"):
                        for col in result["columns"]:
                            st.write(f"- {col}")

                    # Limpiar historial de chat
                    st.session_state.chat_history = []
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ Error: {result.get('error', 'Error desconocido')}")

    st.sidebar.markdown("---")

    # Configuración
    st.sidebar.markdown("## ⚙️ Configuración")

    top_k = st.sidebar.slider(
        "Resultados a recuperar",
        min_value=1,
        max_value=10,
        value=5,
        help="Número de registros más relevantes a considerar"
    )

    use_filters = st.sidebar.checkbox(
        "Usar filtros inteligentes",
        value=True,
        help="El LLM intentará extraer filtros de tu pregunta"
    )

    st.session_state.top_k = top_k
    st.session_state.use_filters = use_filters

    # Estadísticas si hay datos cargados
    if st.session_state.data_loaded:
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 📊 Estadísticas")

        if st.sidebar.button("Ver estadísticas"):
            stats = st.session_state.rag_engine.get_statistics()
            if stats["success"]:
                st.sidebar.metric("Total registros", stats["total_records"])
                st.sidebar.write(f"**Columnas de texto:** {len(stats['text_columns'])}")
                st.sidebar.write(f"**Columnas numéricas:** {len(stats['numeric_columns'])}")

    # Información
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ℹ️ Información")
    st.sidebar.info("""
    **Cómo usar:**
    1. Sube tu archivo Excel
    2. Haz clic en "Procesar Archivo"
    3. Comienza a hacer preguntas

    **Ejemplos de preguntas:**
    - ¿Cuáles son los trabajos mejor pagados?
    - Encuentra empleos remotos
    - ¿Qué empresas están contratando?
    - Muéstrame trabajos de Python
    """)


def main_content():
    """Contenido principal de la aplicación"""
    st.markdown('<div class="main-header">💼 Sistema RAG para Datos de Empleo</div>', unsafe_allow_html=True)

    if not st.session_state.data_loaded:
        st.markdown("""
        <div class="info-box">
            <h3>👋 Bienvenido al Sistema RAG de Empleo</h3>
            <p>Para comenzar, sube un archivo Excel con datos de empleo en la barra lateral.</p>
            <p>El sistema automáticamente:</p>
            <ul>
                <li>Detectará las columnas de tu archivo</li>
                <li>Indexará los datos para búsqueda semántica</li>
                <li>Te permitirá hacer preguntas en lenguaje natural</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar ejemplo de estructura esperada
        with st.expander("📋 Ejemplo de estructura de datos"):
            example_data = {
                "Título": ["Desarrollador Python", "Data Scientist", "DevOps Engineer"],
                "Empresa": ["Tech Corp", "AI Labs", "Cloud Systems"],
                "Ubicación": ["Madrid", "Barcelona", "Remoto"],
                "Salario": [45000, 55000, 50000],
                "Descripción": ["Desarrollo backend...", "Análisis de datos...", "Infraestructura cloud..."]
            }
            st.dataframe(pd.DataFrame(example_data), use_container_width=True)

        return

    # Interfaz de chat
    st.markdown("### 💬 Haz una pregunta sobre los datos")

    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and "results" in message:
                with st.expander(f"📋 Ver {len(message['results'])} registros relevantes"):
                    for i, result in enumerate(message["results"], 1):
                        st.markdown(f"**Registro {i}** (Similitud: {result['score']:.2%})")
                        st.json(result["data"])

    # Input de usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Añadir mensaje del usuario
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Buscando y generando respuesta..."):
                result = st.session_state.rag_engine.query(
                    question=prompt,
                    top_k=st.session_state.get("top_k", 5),
                    use_filters=st.session_state.get("use_filters", True)
                )

                if result["success"]:
                    response = result["response"]
                    st.markdown(response)

                    # Añadir al historial
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "results": result["results"]
                    })

                    # Mostrar resultados expandibles
                    with st.expander(f"📋 Ver {len(result['results'])} registros relevantes"):
                        for i, res in enumerate(result["results"], 1):
                            st.markdown(f"**Registro {i}** (Similitud: {res['score']:.2%})")
                            st.json(res["data"])

                else:
                    error_msg = result.get("error", "Error desconocido")
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"❌ Error: {error_msg}"
                    })

    # Botón para limpiar chat
    if st.session_state.chat_history:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Limpiar conversación", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()


def main():
    """Función principal"""
    initialize_session_state()

    # Verificar API key
    if not os.getenv("GROQ_API_KEY"):
        st.error("""
        ⚠️ **GROQ_API_KEY no configurada**

        Por favor:
        1. Crea un archivo `.env` en la raíz del proyecto
        2. Añade: `GROQ_API_KEY=tu_api_key_aqui`
        3. Obtén tu API key gratis en: https://console.groq.com/keys
        """)
        return

    sidebar()
    main_content()


if __name__ == "__main__":
    main()
