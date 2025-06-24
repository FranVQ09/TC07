import requests
import json

class AgenteOllamaBase:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol
        self.modelo = "llama3.2:3b"  # El modelo que descargamos
        self.url = "http://localhost:11434/api/chat"
    
    def generar_respuesta(self, prompt):
        """Genera una respuesta usando Ollama localmente"""
        try:
            data = {
                "model": self.modelo,
                "messages": [
                    {"role": "system", "content": f"Eres {self.nombre}, un {self.rol}. Responde en español de manera clara y educativa."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            response = requests.post(self.url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error de conexión: {str(e)}. ¿Está Ollama funcionando?"
    
    def presentarse(self):
        return f"Hola, soy {self.nombre}, tu {self.rol}"

class AgenteTutorOllama(AgenteOllamaBase):
    def __init__(self):
        super().__init__("ProfesorAI", "tutor académico especializado en matemáticas")
    
    def explicar_tema(self, tema):
        prompt = f"Explica de manera simple y clara el tema: {tema}. Incluye ejemplos prácticos."
        return self.generar_respuesta(prompt)

class AgenteEvaluadorOllama(AgenteOllamaBase):
    def __init__(self):
        super().__init__("EvaluadorAI", "evaluador que crea preguntas de examen")
    
    def crear_pregunta(self, tema):
        prompt = f"Crea una pregunta de opción múltiple sobre: {tema}. Incluye 4 opciones y la respuesta correcta."
        return self.generar_respuesta(prompt)

class AgenteAsistenteOllama(AgenteOllamaBase):
    def __init__(self):
        super().__init__("AsistenteAI", "asistente que ayuda a resolver dudas")
    
    def resolver_duda(self, pregunta):
        prompt = f"Ayúdame a resolver esta duda paso a paso: {pregunta}"
        return self.generar_respuesta(prompt) 