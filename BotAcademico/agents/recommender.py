# agents/recommender_agent.py

def recommend_resources(query):
    topic = query.lower()

    recomendaciones = {
        "descomposición lu": [
            "Video: https://www.youtube.com/watch?v=yFzZlI1v_O8",
            "Capítulo 5 del libro Álgebra Lineal de Lay"
        ],
        "vectores propios": [
            "https://www.khanacademy.org/math/linear-algebra/eigen-eigenvectors",
            "PDF: Introducción a vectores propios - UNAM"
        ],
        "matriz inversa": [
            "https://es.khanacademy.org/math/algebra/x2f8bb11595b61c86:matrices",
            "PDF: Métodos para hallar la inversa de una matriz"
        ]
    }

    for key in recomendaciones:
        if key in topic:
            return recomendaciones[key]

    return ["No se encontraron recursos específicos, intenta con otro término."]
