from agentes import AgenteTutorOllama, AgenteEvaluadorOllama, AgenteAsistenteOllama

class CoordinadorMultiagentes:
    """
    Coordinador central que gestiona la comunicación y colaboración 
    entre los diferentes agentes del sistema educativo.
    """
    
    def __init__(self):
        print("Inicializando sistema multiagente...")
        self.tutor = AgenteTutorOllama()
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
        """Lista todos los agentes disponibles y sus capacidades"""
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
        """
        Procesa una consulta dirigiéndola al agente apropiado
        y registra la interacción en el historial
        """
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
        
        # Registrar en historial
        resultado = {
            **entrada,
            "agente_usado": agente_usado,
            "respuesta": respuesta
        }
        self.historial.append(resultado)
        
        return respuesta
    
    def colaboracion_agentes(self, tema):
        """
        Demuestra colaboración entre agentes trabajando en el mismo tema
        """
        print(f"\nColaboración de agentes en el tema: '{tema}'")
        print("=" * 60)
        
        # 1. Tutor explica el tema
        print("\nPASO 1: Tutor explica el concepto")
        print("-" * 30)
        explicacion = self.tutor.explicar_tema(tema)
        print(explicacion)
        
        # 2. Evaluador crea una pregunta basada en la explicación
        print("\nPASO 2: Evaluador crea pregunta de evaluación")
        print("-" * 30)
        pregunta = self.evaluador.crear_pregunta(tema)
        print(pregunta)
        
        # 3. Asistente ofrece ayuda adicional
        print("\nPASO 3: Asistente ofrece tips de estudio")
        print("-" * 30)
        ayuda = self.asistente.resolver_duda(f"¿Cómo puedo estudiar mejor {tema}?")
        print(ayuda)
        
        print("\nColaboración completada")
        return True
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de uso del sistema"""
        print(f"\nEstadísticas del Sistema")
        print("=" * 30)
        print(f"Total de consultas: {len(self.historial)}")
        
        # Contar por tipo de agente
        contadores = {"tutor": 0, "evaluador": 0, "asistente": 0}
        for entrada in self.historial:
            if "agente_usado" in entrada:
                contadores[entrada["agente_usado"]] += 1
        
        print("Uso por agente:")
        for agente, count in contadores.items():
            print(f"   {agente.capitalize()}: {count} consultas")
        
        print(f"Última actividad: {self.historial[-1]['timestamp'] if self.historial else 'Ninguna'}")
    
    def _obtener_timestamp(self):
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 