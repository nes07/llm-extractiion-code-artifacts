from neo4j import GraphDatabase
from process import GraphUpdate
import os
from dotenv import load_dotenv
from nodes import ArtifactNode

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


class Neo4jConnection:
    """
    Handles connection to Neo4j and executes queries.
    """

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters)

neo4j_conn = Neo4jConnection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

NODE_TYPE_MAPPING = {
    "QueryNode": "Query",
    "TableNode": "Table",
    "KPINode": "KPI",
    "StatisticNode": "Statistic",
    "APINode": "API",
    "EndpointNode": "Endpoint",
    "DatabaseNode": "Database",
    "VisualizationNode": "Visualization",
    "ArtifactNode": "Artifact"
}

def get_existing_nodes():
    query = """
    MATCH (n)
    WHERE NOT n:Artifact
    RETURN n.id AS id, labels(n) AS tipo, properties(n) AS properties
    """
    with neo4j_conn.driver.session() as session:
        results = session.run(query)
        records = results.data()

    existing_nodes = []
    for record in records:
        node_type = record["tipo"][0] if record["tipo"] else "Unknown"
        node_data = {"id": record["id"], "tipo": node_type, **record["properties"]}
        existing_nodes.append(node_data)

    return existing_nodes

def create_artifact_node(artifact_node):
    """
    Crea un nodo Artifact en Neo4j.
    """
    artifact_query = """
    MERGE (a:Artifact {id: $id})
    SET a.code = $code
    RETURN a
    """
    artifact_params = {"id": artifact_node.id, "code": artifact_node.code}
    neo4j_conn.execute_query(artifact_query, artifact_params)

ALLOW_RELATIONSHIPS_BETWEEN_ARTIFACTNODE = {"APINode", "EndpointNode", "DatabaseNode", "QueryNode", "TableNode", "VisualizationNode"}

def link_artifact_to_nodes(artifact_node: ArtifactNode, knowledge_nodes):
    """
    Links the ArtifactNode to key Nodes.
    """
    print("[Neo4j] Creando relaciones del Artifact con nodos válidos...")

    create_artifact_node(artifact_node)

    for nodo in knowledge_nodes:
        node_class_name = nodo.__class__.__name__

        if node_class_name in ALLOW_RELATIONSHIPS_BETWEEN_ARTIFACTNODE:
            relation_query = """
            MATCH (a:Artifact {id: $artifact_id}), (n {id: $node_id})
            MERGE (a)-[:GENERATED]->(n)
            """
            relation_params = {"artifact_id": artifact_node.id, "node_id": nodo.id}
            neo4j_conn.execute_query(relation_query, relation_params)

    print("[Neo4j] Relaciones del Artifact insertadas correctamente.")

def insert_into_neo4j(graph_update: GraphUpdate):
    """
    Inserts nodes and relationships into Neo4j without checking for duplicates.
    """
    print("[Neo4j] Inserting nodes...")

    for nodo in graph_update.nodos:
        nodo_dict = nodo if isinstance(nodo, dict) else nodo.model_dump()
        node_class_name = nodo.__class__.__name__
        node_label = NODE_TYPE_MAPPING.get(node_class_name, "Unknown")

        if node_label == "Unknown":
            print(f"[Warning] Unrecognized node type: {node_class_name}")
            continue

        query = f"""
        CREATE (n:{node_label} {{ id: $id }})
        SET n += $atributos
        RETURN n
        """
        parameters = {
            "id": nodo_dict["id"],
            "atributos": {k: v for k, v in nodo_dict.items() if k != "id"}
        }
        neo4j_conn.execute_query(query, parameters)

    print("[Neo4j] Inserting relationships...")

    for relacion in graph_update.relaciones:
        relacion_dict = relacion if isinstance(relacion, dict) else relacion.model_dump()

        query = f"""
        MATCH (a {{id: $origen}}), (b {{id: $destino}})
        CREATE (a)-[:{relacion_dict["tipo"]}]->(b)
        """
        parameters = {
            "origen": relacion_dict["origen"],
            "destino": relacion_dict["destino"],
        }
        neo4j_conn.execute_query(query, parameters)

    print("[Neo4j] Data inserted successfully.")

