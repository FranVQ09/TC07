from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import json
import requests
from typing import List
import logging

class EnhancedRetriever:
    def __init__(self, persist_path="enhanced_vectorstore"):
        self.persist_path = persist_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        
    def load_documents_from_directory(self, data_dir="data"):
        """Carga documentos de múltiples formatos desde un directorio"""
        documents = []
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # Cargar archivos de texto
        try:
            txt_loader = DirectoryLoader(
                data_dir, 
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents.extend(txt_loader.load())
        except Exception as e:
            logging.warning(f"Error cargando archivos .txt: {e}")
            
        # Cargar PDFs
        try:
            pdf_loader = DirectoryLoader(
                data_dir,
                glob="**/*.pdf", 
                loader_cls=PyPDFLoader
            )
            documents.extend(pdf_loader.load())
        except Exception as e:
            logging.warning(f"Error cargando archivos .pdf: {e}")
            
        return documents
    
    def add_web_content(self, urls: List[str]):
        """Añade contenido web al vectorstore"""
        documents = []
        
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    doc = Document(
                        page_content=response.text,
                        metadata={"source": url, "type": "web"}
                    )
                    documents.append(doc)
            except Exception as e:
                logging.warning(f"Error descargando {url}: {e}")
                
        return documents
    
    def create_or_update_vectorstore(self, data_dir="data", web_urls=None):
        """Crea o actualiza el vectorstore con contenido dinámico"""
        documents = []
        
        # Cargar documentos locales
        local_docs = self.load_documents_from_directory(data_dir)
        documents.extend(local_docs)
        
        # Añadir contenido web si se proporciona
        if web_urls:
            web_docs = self.add_web_content(web_urls)
            documents.extend(web_docs)
            
        if not documents:
            # Crear contenido básico si no hay documentos
            basic_content = self._create_basic_content()
            documents.extend(basic_content)
        
        # Dividir documentos en chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        split_docs = splitter.split_documents(documents)
        
        # Crear vectorstore
        if os.path.exists(self.persist_path):
            # Actualizar vectorstore existente
            self.vectorstore = Chroma(
                persist_directory=self.persist_path,
                embedding_function=self.embeddings
            )
            self.vectorstore.add_documents(split_docs)
        else:
            # Crear nuevo vectorstore
            self.vectorstore = Chroma.from_documents(
                split_docs,
                embedding=self.embeddings,
                persist_directory=self.persist_path
            )
            
        self.vectorstore.persist()
        print(f"✅ Vectorstore actualizado con {len(split_docs)} chunks")
        
    def _create_basic_content(self):
        """Crea contenido básico cuando no hay documentos disponibles"""
        basic_topics = {
            "algebra_lineal": """
            Álgebra Lineal: Conceptos Fundamentales
            
            Vectores: Un vector es una cantidad que tiene magnitud y dirección. Se representan como listas de números.
            
            Matrices: Una matriz es un arreglo rectangular de números organizados en filas y columnas.
            
            Descomposición LU: Es una factorización de una matriz A = L×U, donde L es triangular inferior y U es triangular superior.
            
            Vectores Propios: Son vectores no nulos que solo cambian de escala cuando se multiplican por una matriz.
            
            Matriz Inversa: Es una matriz que al multiplicarse por la original da la matriz identidad.
            """,
            "calculo": """
            Cálculo: Conceptos Fundamentales
            
            Límites: Describen el comportamiento de una función cuando se acerca a un punto específico.
            
            Derivadas: Miden la tasa de cambio instantánea de una función.
            
            Integrales: Representan el área bajo una curva o la acumulación de cantidades.
            
            Regla de la Cadena: Permite derivar funciones compuestas.
            """,
            "estadistica": """
            Estadística: Conceptos Fundamentales
            
            Media: Es el promedio de un conjunto de datos.
            
            Mediana: Es el valor central de un conjunto ordenado de datos.
            
            Desviación Estándar: Mide la dispersión de los datos respecto a la media.
            
            Distribución Normal: Es una distribución de probabilidad en forma de campana.
            """
        }
        
        documents = []
        for topic, content in basic_topics.items():
            doc = Document(
                page_content=content,
                metadata={"source": f"basic_{topic}", "type": "basic"}
            )
            documents.append(doc)
            
        return documents
    
    def get_retriever(self, k=4):
        """Retorna un retriever configurado"""
        if not self.vectorstore:
            self.vectorstore = Chroma(
                persist_directory=self.persist_path,
                embedding_function=self.embeddings
            )
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
