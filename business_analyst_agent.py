from openai import OpenAI
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel
from typing import List, Dict

openai_client = OpenAI()

class BusinessInsight(BaseModel):
    entity_id: str  # ID of the API, Endpoint, Database, KPI, or Statistic
    description: str  # Business relevance
    key_kpis: List[str]  # Important KPIs (for APIs, Endpoints, Databases)
    statistical_methods: List[str]  # Useful statistical insights

class BusinessAnalysisResponse(BaseModel):
    insights: List[BusinessInsight]

BUSINESS_ANALYST_PROMPT = """
Eres un analista de negocios experto en arquitectura de software y gestión de datos.
Tu tarea es analizar APIs, Endpoints, Bases de Datos, KPIs y Métodos Estadísticos
y proporcionar información clave sobre su relevancia en el negocio.

Para cada entidad:
- **Descripción**: Explica su función en el sistema.
- **KPIs Clave**: Menciona métricas utilizadas para evaluar su rendimiento (para APIs, Endpoints, Bases de Datos).
- **Métodos Estadísticos**: Indica qué análisis pueden aplicarse para interpretar su efectividad.

Ejemplo:
- Una API podría tener KPIs como "Tiempo de Respuesta".
- Un KPI de "Tasa de Mortalidad" en una planta avícola podría requerir análisis de tendencia.
- Un Método Estadístico como "Mediana" se usa para comparar pesos de los pollos procesados.

Devuelve un JSON con la estructura `BusinessAnalysisResponse`.
"""

def analyze_business_context(extracted_entities) -> BusinessAnalysisResponse:
    """
    Uses an AI-powered Business Analyst to generate business insights for APIs, Endpoints, Databases, KPIs, and Statistics.
    """

    dummy_business_response = BusinessAnalysisResponse(
        insights=[]
    )
    return dummy_business_response

    prompt = BUSINESS_ANALYST_PROMPT

    response: ParsedChatCompletion[BusinessAnalysisResponse] = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        response_format=BusinessAnalysisResponse,
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.parsed