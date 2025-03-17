from pydantic import BaseModel, Field
from typing import List, Optional

class ArtifactNode(BaseModel):
    id: str
    code: str

class QueryNode(BaseModel):
    id: str
    pregunta_original: str
    pregunta_generica: str
    sql_query: Optional[str]
    cypher_query: str

class TableNode(BaseModel):
    id: str
    nombre_tabla: str
    columnas: List[str]
    tipos_datos: List[str]

class KPINode(BaseModel):
    id: str
    nombre: str
    descripcion: str

class VisualizationNode(BaseModel):
    id: str
    tipo: str
    eje_x: str
    eje_y: List[str]
    colores: List[str]

class StatisticNode(BaseModel):
    id: str
    name: str
    description: str

class APINode(BaseModel):
    id: str
    name: str
    description: str
    base_url: str

class EndpointNode(BaseModel):
    id: str
    api_id: str
    path: str
    method: str
    parameters: Optional[List[str]]
    description: str

class DatabaseNode(BaseModel):
    id: str
    name: str
    type: str
    description: str
    query_pattern: Optional[str]

class KnowledgeNodesCollection(BaseModel):
    nodos: List[BaseModel]