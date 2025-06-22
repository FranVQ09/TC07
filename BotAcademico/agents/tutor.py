# agents/tutor_agent.py

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def create_tutor_chain(retriever):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain

