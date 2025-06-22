from agents.enhanced_retriever import EnhancedRetriever
from agents.enhanced_tutor import EnhancedTutor
from agents.dynamic_recommender import DynamicRecommender
from dotenv import load_dotenv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

def initialize_system():
    """Inicializa el sistema mejorado"""
    load_dotenv()
    
    print("🚀 Inicializando Bot Académico Mejorado...")
    
    # Inicializar componentes
    retriever_system = EnhancedRetriever()
    recommender = DynamicRecommender()
    
    # URLs de ejemplo para contenido web (opcional)
    web_urls = [
        # Puedes añadir URLs específicas aquí
        # "https://ejemplo.com/algebra-lineal.html"
    ]
    
    # Crear/actualizar vectorstore
    if not os.path.exists(retriever_system.persist_path):
        print("📚 Creando base de conocimiento...")
        retriever_system.create_or_update_vectorstore(web_urls=web_urls)
    else:
        print("📚 Cargando base de conocimiento existente...")
    
    # Configurar tutor
    retriever = retriever_system.get_retriever()
    tutor = EnhancedTutor(retriever)
    
    return tutor, recommender, retriever_system

def add_new_resource_interactive(recommender):
    """Permite añadir recursos interactivamente"""
    print("\n➕ Añadir nuevo recurso:")
    topic = input("Tema: ").strip()
    title = input("Título: ").strip()
    url = input("URL: ").strip()
    description = input("Descripción: ").strip()
    resource_type = input("Tipo (video/libro/articulo/otro): ").strip()
    
    resource = {
        "type": resource_type,
        "title": title,
        "url": url,
        "description": description
    }
    
    recommender.add_resource(topic, resource)
    print("✅ Recurso añadido exitosamente!")

def main():
    try:
        tutor, recommender, retriever_system = initialize_system()
        
        print("\n🎓 Bot Académico Mejorado - Tutor Personalizado")
        print("💡 Comandos especiales:")
        print("   - 'recursos': Añadir nuevo recurso")
        print("   - 'actualizar': Actualizar base de conocimiento")
        print("   - 'salir': Terminar sesión")
        print("=" * 60)
        
        while True:
            query = input("\n🎯 Tu consulta: ").strip()
            
            if query.lower() in ["salir", "exit", "quit"]:
                print("👋 ¡Hasta luego! Sigue aprendiendo.")
                break
                
            elif query.lower() == "recursos":
                add_new_resource_interactive(recommender)
                continue
                
            elif query.lower() == "actualizar":
                print("🔄 Actualizando base de conocimiento...")
                retriever_system.create_or_update_vectorstore()
                print("✅ Base de conocimiento actualizada!")
                continue
                
            elif not query:
                continue
            
            print("\n🤖 Tutor:")
            print("-" * 40)
            
            # Obtener respuesta del tutor
            response = tutor.get_response(query)
            print(response["answer"])
            
            # Mostrar fuentes si están disponibles
            if response["sources"]:
                print(f"\n📋 Fuentes consultadas: {', '.join(set(response['sources']))}")
            
            # Mostrar recomendaciones
            print(f"\n💡 Recomendaciones:")
            print("-" * 40)
            recommendations = recommender.recommend_resources(query)
            for rec in recommendations:
                print(rec)
                print()
            
            print("=" * 60)
            
    except KeyboardInterrupt:
        print("\n\n👋 Sesión terminada por el usuario.")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Error en main: {e}")

if __name__ == "__main__":
    main()