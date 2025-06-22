# agents/retriever_agent.py

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

CHROMA_DIR = "vectorstore"

def create_vector_store(data_path="data/algebra_lineal.txt", persist_path=CHROMA_DIR):
    loader = TextLoader(data_path)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_path)
    vectorstore.persist()
    print("✅ Vectorstore Chroma creado.")

def load_retriever(persist_path=CHROMA_DIR):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=persist_path, embedding_function=embeddings)
    return vectorstore.as_retriever()
