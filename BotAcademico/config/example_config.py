# config/example_config.py
"""
Archivo de configuración de ejemplo para personalizar el comportamiento del bot
"""

# Configuración del modelo
MODEL_CONFIG = {
    "model_name": "gpt-4o",
    "temperature": 0.3,
    "max_tokens": 1000
}

# Configuración del retriever
RETRIEVER_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "k_documents": 4
}

# Temas soportados por defecto
SUPPORTED_TOPICS = [
    "algebra_lineal",
    "calculo",
    "estadistica",
    "geometria",
    "trigonometria",
    "probabilidad"
]

# URLs de recursos educativos confiables
TRUSTED_SOURCES = [
    "https://es.khanacademy.org",
    "https://www.coursera.org",
    "https://www.edx.org",
    "https://ocw.mit.edu"
]