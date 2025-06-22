from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

class EnhancedTutor:
    def __init__(self, retriever, model_name="gpt-4o"):
        self.retriever = retriever
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.3)
        self.chain = self._create_chain()
        
    def _create_chain(self):
        """Crea una cadena de QA mejorada con prompt personalizado"""
        
        template = """Eres un tutor académico experto y amigable. Tu objetivo es ayudar a los estudiantes a entender conceptos complejos de manera clara y accesible.

Contexto relevante:
{context}

Pregunta del estudiante: {question}

Instrucciones para tu respuesta:
1. Responde de manera clara y pedagógica
2. Usa ejemplos cuando sea apropiado
3. Si no encuentras información específica en el contexto, usa tu conocimiento general pero indícalo
4. Sugiere pasos de seguimiento o práctica cuando sea relevante
5. Mantén un tono amigable y motivador

Respuesta:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def get_response(self, query: str) -> Dict:
        """Obtiene respuesta del tutor con información adicional"""
        with get_openai_callback() as cb:
            result = self.chain({"query": query})
            
        return {
            "answer": result["result"],
            "sources": [doc.metadata.get("source", "Desconocido") for doc in result["source_documents"]],
            "tokens_used": cb.total_tokens,
            "cost": cb.total_cost
        }