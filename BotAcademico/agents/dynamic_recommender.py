import json
import os
from typing import List, Dict
import requests
from datetime import datetime

class DynamicRecommender:
    def __init__(self, config_file="config/resources.json"):
        self.config_file = config_file
        self.resources = self._load_resources()
        
    def _load_resources(self) -> Dict:
        """Carga recursos desde archivo de configuración"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._create_default_resources()
    
    def _create_default_resources(self) -> Dict:
        """Crea recursos por defecto"""
        default_resources = {
            "algebra_lineal": {
                "keywords": ["matriz", "vector", "determinante", "eigenvalor", "eigenvector", "lu", "inversa"],
                "resources": [
                    {
                        "type": "video",
                        "title": "Álgebra Lineal - Khan Academy",
                        "url": "https://es.khanacademy.org/math/linear-algebra",
                        "description": "Curso completo de álgebra lineal"
                    },
                    {
                        "type": "libro",
                        "title": "Álgebra Lineal - David Lay",
                        "url": "https://www.pearson.com/store/p/linear-algebra-and-its-applications/P100000843349",
                        "description": "Libro de referencia estándar"
                    }
                ]
            },
            "calculo": {
                "keywords": ["derivada", "integral", "limite", "continuidad", "diferencial"],
                "resources": [
                    {
                        "type": "video",
                        "title": "Cálculo - Khan Academy",
                        "url": "https://es.khanacademy.org/math/calculus-1",
                        "description": "Curso de cálculo diferencial e integral"
                    }
                ]
            },
            "estadistica": {
                "keywords": ["media", "mediana", "varianza", "probabilidad", "distribucion"],
                "resources": [
                    {
                        "type": "video",
                        "title": "Estadística - Khan Academy", 
                        "url": "https://es.khanacademy.org/math/statistics-probability",
                        "description": "Curso de estadística y probabilidad"
                    }
                ]
            }
        }
        
        # Guardar recursos por defecto
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_resources, f, indent=2, ensure_ascii=False)
            
        return default_resources
    
    def add_resource(self, topic: str, resource: Dict):
        """Añade un nuevo recurso dinámicamente"""
        if topic not in self.resources:
            self.resources[topic] = {"keywords": [], "resources": []}
            
        self.resources[topic]["resources"].append(resource)
        self._save_resources()
        
    def _save_resources(self):
        """Guarda recursos en archivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, indent=2, ensure_ascii=False)
    
    def recommend_resources(self, query: str) -> List[str]:
        """Recomienda recursos basado en la consulta"""
        query_lower = query.lower()
        recommendations = []
        
        # Buscar coincidencias en palabras clave
        for topic, data in self.resources.items():
            for keyword in data["keywords"]:
                if keyword in query_lower:
                    for resource in data["resources"]:
                        rec_text = f"📚 {resource['title']} ({resource['type']})\n   🔗 {resource['url']}\n   📝 {resource['description']}"
                        recommendations.append(rec_text)
                    break
                    
        if not recommendations:
            recommendations = [
                "🔍 No encontré recursos específicos para tu consulta.",
                "💡 Intenta reformular tu pregunta o usar términos más específicos.",
                "📚 Recursos generales disponibles: álgebra lineal, cálculo, estadística"
            ]
            
        return recommendations[:3]  # Limitar a 3 recomendaciones