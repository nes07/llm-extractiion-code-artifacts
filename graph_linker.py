from nodes import (
    ArtifactNode, UserNode, DesignMemoryNode,
    APINode, EndpointNode, QueryNode, TableNode, KPINode,
)
from insertion import (
    create_artifact_node,
    create_user_node,
    create_design_memory_node,
    create_api_node,
    create_endpoint_node,
    create_query_node,
    create_table_node,
    create_kpi_node,
)

class GraphLinker:
    _node_creator_map = {
        UserNode: create_user_node,
        ArtifactNode: create_artifact_node,
        DesignMemoryNode: create_design_memory_node,
        APINode: create_api_node,
        EndpointNode: create_endpoint_node,
        QueryNode: create_query_node,
        TableNode: create_table_node,
        KPINode: create_kpi_node,
    }

    @staticmethod
    def ensure_node_created(node):
        """
        Ejecuta la función de creación apropiada para el tipo de nodo.
        """
        creator = GraphLinker._node_creator_map.get(type(node))
        if creator is None:
            raise ValueError(f"No se reconoce el tipo de nodo: {type(node)}")
        creator(node)

    @staticmethod
    def link(source, target, relation_type: str):
        """
        Crea una relación entre dos nodos asegurando primero que existan.
        """
        GraphLinker.ensure_node_created(source)
        GraphLinker.ensure_node_created(target)

        source_label = source.__class__.__name__.replace("Node", "")
        target_label = target.__class__.__name__.replace("Node", "")

        query = f"""
        MATCH (a:{source_label} {{id: $source_id}}),
              (b:{target_label} {{id: $target_id}})
        MERGE (a)-[:{relation_type}]->(b)
        """
        params = {"source_id": source.id, "target_id": target.id}
        neo4j_conn.execute_query(query, params)

        print(f"[Neo4j] Relación {relation_type} creada: ({source_label})-[:{relation_type}]->({target_label})")