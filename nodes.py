from pydantic import BaseModel, PrivateAttr
from typing import List, Optional
from datetime import datetime

class ArtifactNode(BaseModel):
    id: str
    code: str
    _code_embedding: Optional[List[float]] = PrivateAttr(default=None)

class UserNode(BaseModel):
    id: str

class QueryNode(BaseModel):
    id: str
    pregunta_original: str
    pregunta_generica: str
    sql_query: Optional[str]
    cypher_query: str

    _pregunta_original_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _pregunta_generica_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _sql_query_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _cypher_query_embedding: Optional[List[float]] = PrivateAttr(default=None)

class TableNode(BaseModel):
    id: str
    nombre_tabla: str
    columnas: List[str]
    tipos_datos: List[str]

    _nombre_tabla_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _columnas_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _tipos_datos_embedding: Optional[List[float]] = PrivateAttr(default=None)

class KPINode(BaseModel):
    id: str
    nombre: str
    descripcion: str

    _nombre_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _descripcion_embedding: Optional[List[float]] = PrivateAttr(default=None)

class VisualizationNode(BaseModel):
    id: str
    tipo: str
    eje_x: str
    eje_y: List[str]
    colores: List[str]

    _tipo_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _eje_x_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _eje_y_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _colores_embedding: Optional[List[float]] = PrivateAttr(default=None)

class StatisticNode(BaseModel):
    id: str
    name: str
    description: str

    _name_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _description_embedding: Optional[List[float]] = PrivateAttr(default=None)

class APINode(BaseModel):
    id: str
    name: str
    description: str
    base_url: str

    _name_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _description_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _base_url_embedding: Optional[List[float]] = PrivateAttr(default=None)

class EndpointNode(BaseModel):
    id: str
    api_id: str
    path: str
    method: str
    parameters: Optional[List[str]]
    description: str

    _api_id_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _path_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _method_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _parameters_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _description_embedding: Optional[List[float]] = PrivateAttr(default=None)

class DatabaseNode(BaseModel):
    id: str
    name: str
    type: str
    description: str
    query_pattern: Optional[str]

    _name_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _type_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _description_embedding: Optional[List[float]] = PrivateAttr(default=None)
    _query_pattern_embedding: Optional[List[float]] = PrivateAttr(default=None)

class KnowledgeNodesCollection(BaseModel):
    nodos: List[BaseModel]