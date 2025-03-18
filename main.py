import uuid
from extract import extract_metadata_with_retries
from business_analyst_agent import analyze_business_context
from nodes_generator import generate_knowledge_nodes
from relationship_agent import determine_relationships
from insertion import insert_into_neo4j, get_existing_nodes, link_artifact_to_nodes
from process import GraphUpdate
from nodes import ArtifactNode

def process_artifact(artifact_code: str):
    """
    Processes an artifact provided as a string instead of reading from a file.
    """
    print("[Paso 1] Recibiendo el código del artifact...")

    if not artifact_code:
        raise ValueError("El código del artifact está vacío.")

    print("[Paso 2] Extrayendo información del código...")
    extracted_entities = extract_metadata_with_retries(artifact_code)

    print("APIs detectadas:", extracted_entities.apis)
    print("Endpoints detectados:", extracted_entities.endpoints)
    print("Bases de datos detectadas:", extracted_entities.databases)
    print("Consultas SQL detectadas:", extracted_entities.queries)
    print("Tablas detectadas:", extracted_entities.tables)
    print("Relaciones detectadas:", extracted_entities.relationships)

    print("[Paso 3] Generando contexto de negocio para APIs, Endpoints, Bases de Datos, KPIs y Estadísticas...")
    business_contexts = analyze_business_context(extracted_entities)

    print("[Paso 4] Generando nodos a partir de las entidades extraídas...")
    knowledge_nodes = generate_knowledge_nodes(extracted_entities, business_contexts)

    print("[Paso 5] Obteniendo nodos existentes de la base...")
    existing_nodes = []

    print("[Paso 6] Evaluando relaciones entre todos los nodos...")
    knowledge_relationships = determine_relationships(
        knowledge_nodes.nodos,
        existing_nodes
    )

    print("[Paso 7] Insertando nodos y relaciones en Neo4j...")

    artifact_id = str(uuid.uuid4())
    artifact_node = ArtifactNode(id=artifact_id, code=artifact_code)

    graph_update = GraphUpdate(
        nodos=[node.model_dump() for node in knowledge_nodes.nodos],
        relaciones=[rel.model_dump() for rel in knowledge_relationships.relaciones]
    )
    insert_into_neo4j(graph_update)

    link_artifact_to_nodes(artifact_node, knowledge_nodes.nodos)

    return {
        "artifact_id": artifact_id,
        "message": "Artifact processed successfully",
        "nodes_inserted": len(knowledge_nodes.nodos),
        "relationships_inserted": len(knowledge_relationships.relaciones)
    }