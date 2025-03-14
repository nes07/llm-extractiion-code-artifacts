import uuid
import argparse
from extract import extract_metadata_with_retries
from business_analyst_agent import analyze_business_context
from nodes_generator import generate_knowledge_nodes
from relationship_agent import determine_relationships
from insertion import insert_into_neo4j, get_existing_nodes, link_artifact_to_nodes
from process import GraphUpdate
from nodes import ArtifactNode

def read_file(file_path: str) -> str:
    """
    Lee el contenido del archivo con el código del artifact.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Procesa un archivo con código de artifacts y almacena los datos en Neo4j.")
    parser.add_argument("file_path", type=str, help="Ruta al archivo con el código del artifact.")
    parser.add_argument("--dry-run", action="store_true", help="Simula el procesamiento sin insertar en Neo4j.")
    
    args = parser.parse_args()
    file_path = args.file_path

    print("[Paso 1] Leyendo el archivo...")
    artifact_code = read_file(file_path)

    if not artifact_code:
        print("El archivo está vacío. Finalizando.")
        exit(0)

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

    if args.dry_run:
        print("\nModo Dry-Run Activado: No se insertará en Neo4j.")
        print("Nodos Generados:", knowledge_nodes)
        print("Relaciones Generadas:", knowledge_relationships)
        print("Cantidad de Nodos:", len(knowledge_nodes.nodos))
        print("Cantidad de Relaciones:", len(knowledge_relationships.relaciones))
        exit(0)

    print("[Paso 7] Insertando nodos y relaciones en Neo4j...")

    artifact_id = str(uuid.uuid4())
    artifact_node = ArtifactNode(id=artifact_id, code=artifact_code)

    graph_update = GraphUpdate(
        nodos=[node.model_dump() for node in knowledge_nodes.nodos],
        relaciones=[rel.model_dump() for rel in knowledge_relationships.relaciones]
    )
    insert_into_neo4j(graph_update)

    link_artifact_to_nodes(artifact_node, knowledge_nodes.nodos)

if __name__ == "__main__":
    main()