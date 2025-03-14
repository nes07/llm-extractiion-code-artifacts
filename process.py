from typing import List, Union
from pydantic import BaseModel
from relations import KnowledgeRelationship
from nodes import APINode, EndpointNode, DatabaseNode, QueryNode, TableNode, ArtifactNode, KPINode, StatisticNode

class GraphUpdate(BaseModel):
    """
    Represents the structured output of processed nodes and relationships.
    """
    nodos: List[Union[ArtifactNode, APINode, EndpointNode, DatabaseNode, QueryNode, TableNode, KPINode, StatisticNode]]
    relaciones: List[KnowledgeRelationship]