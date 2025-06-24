# main.py
from coordinador import CoordinadorMultiagentes

def main():
    print("¡Sistema de Multiagentes con OLLAMA! (100% GRATIS)")
    print("=" * 60)
    print("Usando IA local - Sin costos, sin límites!\n")

    # Seleccionar modo
    usar_rag = input("¿Quieres activar RAG (uso de apuntes)? (s/n): ").strip().lower() == "s"
    coordinador = CoordinadorMultiagentes(usar_rag=usar_rag)
    
    tutor = coordinador.tutor
    evaluador = coordinador.evaluador  
    asistente = coordinador.asistente
    
    print("\nAgentes disponibles:")
    print(f"1. {tutor.presentarse()}")
    print(f"2. {evaluador.presentarse()}")
    print(f"3. {asistente.presentarse()}")
    
    while True:
        print("\n" + "=" * 60)
        print("¿Qué quieres hacer?")
        print("1. Explicar un tema (Tutor)")
        print("2. Crear pregunta de examen (Evaluador)")
        print("3. Resolver una duda (Asistente)")
        print("4. Ver colaboración entre agentes")
        print("5. Ver estadísticas del sistema")
        print("6. Salir")
        
        opcion = input("\nElige una opción (1-6): ").strip()
        
        if opcion == "1":
            tema = input("¿Qué tema quieres que explique? ")
            print(f"\n{tutor.nombre} está pensando...")
            respuesta = tutor.explicar_tema(tema)
            print(f"\n{tutor.nombre} dice:\n" + "-" * 40)
            print(respuesta)
            
        elif opcion == "2":
            tema = input("¿Sobre qué tema quieres la pregunta? ")
            print(f"\n{evaluador.nombre} está creando...")
            respuesta = evaluador.crear_pregunta(tema)
            print(f"\n{evaluador.nombre} dice:\n" + "-" * 40)
            print(respuesta)
            
        elif opcion == "3":
            duda = input("¿Cuál es tu duda? ")
            print(f"\n{asistente.nombre} está analizando...")
            respuesta = asistente.resolver_duda(duda)
            print(f"\n{asistente.nombre} dice:\n" + "-" * 40)
            print(respuesta)
            
        elif opcion == "4":
            tema = input("¿Sobre qué tema quieres ver la colaboración? ")
            coordinador.colaboracion_agentes(tema)
            
        elif opcion == "5":
            coordinador.mostrar_estadisticas()
            
        elif opcion == "6":
            print("\n¡Hasta luego! Gracias por usar el sistema de multiagentes.")
            break
            
        else:
            print("\nOpción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
