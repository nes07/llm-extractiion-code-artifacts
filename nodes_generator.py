import os
import uuid
from openai import OpenAI
from nodes import (
    KnowledgeNodesCollection, QueryNode, VisualizationNode, 
    APINode, EndpointNode, DatabaseNode, TableNode, 
    KPINode, StatisticNode
)
from business_analyst_agent import BusinessAnalysisResponse

def embed_with_openai_large(text: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY no está definido en el archivo .env")

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

def add_private_embeddings(node):
    for field, value in node.__dict__.items():
        if field == "id":
            continue

        private_attr = f"_{field}_embedding"

        if isinstance(value, str) and value.strip():
            setattr(node, private_attr, embed_with_openai_large(value))
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            joined = " ".join(value)
            setattr(node, private_attr, embed_with_openai_large(joined))
    return node

def generate_knowledge_nodes(extracted_entities, business_context) -> KnowledgeNodesCollection:
    """
    Converts extracted entities and business analysis insights into knowledge nodes, ensuring unique IDs,
    and adds private embedding fields for all applicable properties (except 'id').
    """
    nodes = []

    for api in extracted_entities.apis:
        api_node = APINode(
            id=str(uuid.uuid4()),
            name=api.name,
            description=api.description,
            base_url=api.base_url
        )
        nodes.append(add_private_embeddings(api_node))

    for endpoint in extracted_entities.endpoints:
        endpoint_node = EndpointNode(
            id=str(uuid.uuid4()),
            api_id=str(uuid.uuid4()),
            path=endpoint.path,
            method=endpoint.method,
            parameters=endpoint.parameters or [],
            description=endpoint.description
        )
        nodes.append(add_private_embeddings(endpoint_node))

    for db in extracted_entities.databases:
        db_node = DatabaseNode(
            id=str(uuid.uuid4()),
            name=db.name,
            type=db.type,
            description=db.description,
            query_pattern=db.query_pattern or ""
        )
        nodes.append(add_private_embeddings(db_node))

    for table in extracted_entities.tables:
        table_node = TableNode(
            id=str(uuid.uuid4()),
            nombre_tabla=table.nombre_tabla,
            columnas=table.columnas,
            tipos_datos=table.tipos_datos
        )
        nodes.append(add_private_embeddings(table_node))

    for query in extracted_entities.queries:
        query_node = QueryNode(
            id=str(uuid.uuid4()),
            pregunta_original=query.pregunta_original,
            pregunta_generica=query.pregunta_generica,
            sql_query=query.sql_query or "",
            cypher_query=query.cypher_query or ""
        )
        nodes.append(add_private_embeddings(query_node))

    if business_context and business_context.insights:
        for insight in business_context.insights:

            if insight.key_kpis:
                for kpi in insight.key_kpis:
                    kpi_node = KPINode(
                        id=str(uuid.uuid4()),
                        nombre=kpi,
                        descripcion=f"KPI clave en faenación de pollos: {kpi}"
                    )
                    nodes.append(add_private_embeddings(kpi_node))

            if insight.statistical_methods:
                for stat in insight.statistical_methods:
                    stat_node = StatisticNode(
                        id=str(uuid.uuid4()),
                        name=stat,
                        description=f"Método estadístico relevante en producción avícola: {stat}"
                    )
                    nodes.append(add_private_embeddings(stat_node))

    return KnowledgeNodesCollection(nodos=nodes)