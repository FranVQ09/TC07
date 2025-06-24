# rag.py
from sentence_transformers import SentenceTransformer
import faiss
import os

class RAG:
    def __init__(self, carpeta_docs):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.textos = []
        self._cargar_y_indexar_desde_carpeta(carpeta_docs)
    
    def _cargar_y_indexar_desde_carpeta(self, carpeta):
        textos = []
        for nombre_archivo in os.listdir(carpeta):
            if nombre_archivo.endswith(".txt"):
                ruta = os.path.join(carpeta, nombre_archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    partes = [p.strip() for p in contenido.split("\n\n") if p.strip()]
                    textos.extend(partes)
        self.textos = textos
        vectores = self.model.encode(textos)
        self.index = faiss.IndexFlatL2(len(vectores[0]))
        self.index.add(vectores)

    def recuperar_contexto(self, consulta, k=3):
        q_vector = self.model.encode([consulta])
        _, indices = self.index.search(q_vector, k)
        contexto = "\n".join([self.textos[i] for i in indices[0]])
        return contexto
