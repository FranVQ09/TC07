# main.py

from agents.retriever import create_vector_store, load_retriever
from agents.tutor import create_tutor_chain
from agents.recommender import recommend_resources
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    if not os.path.exists("vectorstore"):
        print("Creando base vectorial...")
        create_vector_store()

    print("Cargando sistema...")
    retriever = load_retriever()
    tutor_chain = create_tutor_chain(retriever)

    print("\nBienvenido a Bot Académico - Tutor Académico Personalizado")
    print("Escribe tu pregunta o 'salir' para terminar.\n")

    while True:
        query = input("Estudiante: ")
        if query.lower() in ["salir", "exit", "quit"]:
            print("Hasta luego.")
            break

        print("\nTutor:")
        result = tutor_chain.run(query)
        print(result)

        print("\nRecomendaciones:")
        for r in recommend_resources(query):
            print(f"- {r}")

        print("-" * 50)

if __name__ == "__main__":
    main()
