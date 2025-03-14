from pydantic import BaseModel
from typing import List

POSSIBLE_RELATIONSHIPS = [
    {"origen": "APINode", "destino": "EndpointNode", "tipo": "EXPOSES"},
    {"origen": "EndpointNode", "destino": "DatabaseNode", "tipo": "QUERIES"},
    {"origen": "QueryNode", "destino": "EndpointNode", "tipo": "CALLS"},
    {"origen": "QueryNode", "destino": "DatabaseNode", "tipo": "READS_FROM"},
    {"origen": "DatabaseNode", "destino": "TableNode", "tipo": "STORES"},
    {"origen": "TableNode", "destino": "QueryNode", "tipo": "USES"},
    {"origen": "TableNode", "destino": "VisualizationNode", "tipo": "USES"},
    {"origen": "TableNode", "destino": "KPINode", "tipo": "CONTAINS_DATA_FOR"},
    {"origen": "KPINode", "destino": "StatisticNode", "tipo": "DERIVED_FROM"},
    {"origen": "StatisticNode", "destino": "VisualizationNode", "tipo": "REPRESENTS"}
]

class KnowledgeRelationship(BaseModel):
    origen: str
    destino: str
    tipo: str

class KnowledgeRelationshipsCollection(BaseModel):
    relaciones: List[KnowledgeRelationship]