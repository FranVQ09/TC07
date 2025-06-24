from agentes import AgenteTutorOllama, AgenteEvaluadorOllama, AgenteAsistenteOllama

def main():
    print("🤖 ¡Sistema de Multiagentes con OLLAMA! (100% GRATIS)")
    print("=" * 60)
    print("🚀 Usando IA local - Sin costos, sin límites!")
    
    # Crear los agentes con Ollama
    print("\n⏳ Inicializando agentes...")
    tutor = AgenteTutorOllama()
    evaluador = AgenteEvaluadorOllama()
    asistente = AgenteAsistenteOllama()
    print("✅ ¡Agentes listos!")
    
    # Presentar los agentes
    print("\n👥 Agentes disponibles:")
    print(f"1. {tutor.presentarse()}")
    print(f"2. {evaluador.presentarse()}")
    print(f"3. {asistente.presentarse()}")
    
    while True:
        print("\n" + "=" * 60)
        print("🎯 ¿Qué quieres hacer?")
        print("1. 🎓 Explicar un tema (Tutor)")
        print("2. 📝 Crear pregunta de examen (Evaluador)")
        print("3. 💡 Resolver una duda (Asistente)")
        print("4. 🚪 Salir")
        
        opcion = input("\n👉 Elige una opción (1-4): ").strip()
        
        if opcion == "1":
            tema = input("📚 ¿Qué tema quieres que explique? ")
            print(f"\n🎓 {tutor.nombre} está pensando...")
            respuesta = tutor.explicar_tema(tema)
            print(f"\n💬 {tutor.nombre} dice:")
            print("-" * 40)
            print(respuesta)
            
        elif opcion == "2":
            tema = input("📋 ¿Sobre qué tema quieres la pregunta? ")
            print(f"\n📝 {evaluador.nombre} está creando...")
            respuesta = evaluador.crear_pregunta(tema)
            print(f"\n💬 {evaluador.nombre} dice:")
            print("-" * 40)
            print(respuesta)
            
        elif opcion == "3":
            duda = input("❓ ¿Cuál es tu duda? ")
            print(f"\n💡 {asistente.nombre} está analizando...")
            respuesta = asistente.resolver_duda(duda)
            print(f"\n💬 {asistente.nombre} dice:")
            print("-" * 40)
            print(respuesta)
            
        elif opcion == "4":
            print("\n👋 ¡Hasta luego! Gracias por usar el sistema de multiagentes")
            break
            
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main() 