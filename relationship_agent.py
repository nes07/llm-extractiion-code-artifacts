from relations import KnowledgeRelationshipsCollection, POSSIBLE_RELATIONSHIPS, KnowledgeRelationship
from nodes import ArtifactNode
from openai import OpenAI
from openai.types.chat import ParsedChatCompletion

openai_client = OpenAI()


def determine_relationships(nodos, existing_nodes) -> KnowledgeRelationshipsCollection:
    """
    Evaluates relationships between new and existing nodes, ensuring they match POSSIBLE_RELATIONSHIPS.
    """
    prompt = f"""
    Eres un analista experto en grafos de conocimiento. Tienes una lista de nodos nuevos y existentes,
    y tu tarea es determinar las relaciones entre ellos basándote en las reglas definidas.

    **Datos Proporcionados:**
    - **Nodos Nuevos:** {nodos}
    - **Nodos Existentes en la Base:** {existing_nodes}

    **Reglas de Relación (POSSIBLE_RELATIONSHIPS):**
    {POSSIBLE_RELATIONSHIPS}

    **Criterios Importantes:**
    - **No crees relaciones entre nodos que no tienen conexión lógica real en los datos.**
    - **Verifica que las queries y bases de datos realmente se refieran entre sí antes de crear una relación.**
    - **Solo asigna relaciones si los identificadores de los nodos coinciden en estructura o contexto.**
    - **Evita unir artifacts distintos que no comparten elementos comunes.**
    - **Las relaciones deben reflejar conexiones reales, no inferencias.**

    **Formato de Respuesta:**
    Devuelve un JSON en la estructura `KnowledgeRelationshipsCollection`:
    ```json
    {{
        "relaciones": [
            {{"origen": "node_id_1", "destino": "node_id_2", "tipo": "RELATION_TYPE"}},
            ...
        ]
    }}
    ```
    """

    response: ParsedChatCompletion[KnowledgeRelationshipsCollection] = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        response_format=KnowledgeRelationshipsCollection,
        messages=[{"role": "system", "content": prompt}]
    )

    suggested_relationships = response.choices[0].message.parsed.relaciones

    return KnowledgeRelationshipsCollection(relaciones=suggested_relationships)