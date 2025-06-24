# coordinador.py
from agentes import AgenteTutorOllama, AgenteEvaluadorOllama, AgenteAsistenteOllama
from datetime import datetime

class CoordinadorMultiagentes:
    def __init__(self, usar_rag=False):
        print("Inicializando sistema multiagente...")
        self.tutor = AgenteTutorOllama(usar_rag=usar_rag)
        self.evaluador = AgenteEvaluadorOllama()
        self.asistente = AgenteAsistenteOllama()
        self.agentes = {
            "tutor": self.tutor,
            "evaluador": self.evaluador,
            "asistente": self.asistente
        }
        self.historial = []
        print("Sistema multiagente inicializado")
    
    def listar_agentes(self):
        print("\nAgentes del Sistema:")
        print("-" * 40)
        for nombre, agente in self.agentes.items():
            print(f"{agente.presentarse()}")
            if nombre == "tutor":
                print("Capacidades: Explicar conceptos, dar ejemplos, enseñar")
            elif nombre == "evaluador":
                print("Capacidades: Crear exámenes, generar preguntas, evaluar")
            elif nombre == "asistente":
                print("Capacidades: Resolver dudas, asistir paso a paso")
        print()

    def procesar_consulta(self, tipo_consulta, contenido):
        entrada = {
            "tipo": tipo_consulta,
            "consulta": contenido,
            "timestamp": self._obtener_timestamp()
        }
        
        if tipo_consulta == "explicacion":
            respuesta = self.tutor.explicar_tema(contenido)
            agente_usado = "tutor"
        elif tipo_consulta == "evaluacion":
            respuesta = self.evaluador.crear_pregunta(contenido)
            agente_usado = "evaluador"
        elif tipo_consulta == "asistencia":
            respuesta = self.asistente.resolver_duda(contenido)
            agente_usado = "asistente"
        else:
            return "Tipo de consulta no reconocido"
        
        resultado = {
            **entrada,
            "agente_usado": agente_usado,
            "respuesta": respuesta
        }
        self.historial.append(resultado)
        return respuesta

    def colaboracion_agentes(self, tema):
        print(f"\nColaboración de agentes en el tema: '{tema}'")
        print("=" * 60)
        
        print("\nPASO 1: Tutor explica el concepto")
        print("-" * 30)
        print(self.tutor.explicar_tema(tema))
        
        print("\nPASO 2: Evaluador crea pregunta de evaluación")
        print("-" * 30)
        print(self.evaluador.crear_pregunta(tema))
        
        print("\nPASO 3: Asistente ofrece tips de estudio")
        print("-" * 30)
        print(self.asistente.resolver_duda(f"¿Cómo puedo estudiar mejor {tema}?"))
        
        print("\nColaboración completada")
        return True

    def mostrar_estadisticas(self):
        print(f"\nEstadísticas del Sistema")
        print("=" * 30)
        print(f"Total de consultas: {len(self.historial)}")
        contadores = {"tutor": 0, "evaluador": 0, "asistente": 0}
        for entrada in self.historial:
            if "agente_usado" in entrada:
                contadores[entrada["agente_usado"]] += 1
        print("Uso por agente:")
        for agente, count in contadores.items():
            print(f"   {agente.capitalize()}: {count} consultas")
        print(f"Última actividad: {self.historial[-1]['timestamp'] if self.historial else 'Ninguna'}")

    def _obtener_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
