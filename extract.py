from openai import OpenAI
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel
from typing import List, Optional
from nodes import APINode, EndpointNode, DatabaseNode, QueryNode, TableNode, KPINode, StatisticNode
from relations import KnowledgeRelationshipsCollection, KnowledgeRelationship
from dotenv import load_dotenv

load_dotenv()

openai_api_client = OpenAI()

class ExtractedEntities(BaseModel):
    apis: List[APINode]
    endpoints: List[EndpointNode]
    databases: List[DatabaseNode]
    queries: List[QueryNode]
    tables: List[TableNode]
    relationships: KnowledgeRelationshipsCollection

EXTRACTION_PROMPT = """You are an advanced code analyzer specialized in extracting APIs, endpoints, database interactions, tables, and queries from source code.
The provided code will contain UI components, charts, and data processing logic.

As a note: you **WILL ONLY EXTRACT THE ELEMENTS LISTED ON THE CLASS**. Nothing else.

Your task is to extract the following elements **explicitly** found in the provided code:
- **APIs**: Identify external or internal APIs used in `fetch()`, `axios`, or other HTTP request libraries.
- **Endpoints**: Extract the specific **URL**, **HTTP method**, and **parameters**.
- **Queries**: Identify SQL/NoSQL queries, ORM interactions, or API-based query mechanisms.
- **Databases**: Detect database usage, including SQL, NoSQL, Firebase, IndexedDB, or other storage solutions.
- **Tables**: **Identify specific tables being referenced in queries or API requests, including column names and data types. If you find queries, then you should also identify the tables they interact with. This 
tables are right after the FROM clause in the SQL queries.** FIND THEM.

⚠ **Only return elements that are explicitly present in the provided code. Do not infer or assume APIs, queries, or databases that are not explicitly stated.**

---

### **Example Code Artifact (React + Recharts + API Calls + Database Queries)**
```javascript
import React, {{ useState, useEffect }} from 'react';
import {{ Table, Thead, Tbody, Tr, Th, Td }} from '@/components/ui/table';

// API Configuration
const API_BASE_URL = "https://api.ordersystem.com";

const OrderTable = () => {{
    const [orders, setOrders] = useState([]);

    useEffect(() => {{
        fetch(`${{API_BASE_URL}}/orders`)
            .then(response => response.json())
            .then(data => setOrders(data))
            .catch(error => console.error("Error fetching order data:", error));
    }}, []);

    return (
        <Table>
            <Thead>
                <Tr>
                    <Th>Order ID</Th>
                    <Th>Customer Name</Th>
                    <Th>Total</Th>
                </Tr>
            </Thead>
            <Tbody>
                {{orders.map((order, index) => (
                    <Tr key={{index}}>
                        <Td>{{order.id}}</Td>
                        <Td>{{order.customer_name}}</Td>
                        <Td>${{order.total}}</Td>
                    </Tr>
                ))}}
            </Tbody>
        </Table>
    );
}};

export default OrderTable;
```

---

### **Expected Extracted JSON Output**
```json
{{
    "apis": [
        {{
            "id": "api_1",
            "name": "Order System API",
            "description": "API for managing customer orders",
            "base_url": "https://api.ordersystem.com"
        }}
    ],
    "endpoints": [
        {{
            "id": "endpoint_1",
            "api_id": "api_1",
            "path": "/orders",
            "method": "GET",
            "parameters": []
        }}
    ],
    "databases": [
        {{
            "id": "db_1",
            "name": "OrdersDB",
            "type": "SQL",
            "description": "Primary database for order management",
            "query_pattern": "SELECT * FROM orders WHERE id = ?"
        }}
    ],
    "queries": [
        {{
            "id": "query_1",
            "pregunta_original": "Retrieve all customer orders",
            "pregunta_generica": "Fetch order records",
            "sql_query": "SELECT * FROM orders",
            "cypher_query": ""
        }},
        {{
            "id": "query_2",
            "pregunta_original": "Get total sales by region",
            "pregunta_generica": "Fetch regional sales summary",
            "sql_query": "SELECT region, SUM(total_sales) FROM orders GROUP BY region",
            "cypher_query": ""
        }}
    ],
    "tables": [
        {{
            "id": "table_1",
            "nombre_tabla": "orders",
            "columnas": ["id", "customer_name", "total", "region", "total_sales"],
            "tipos_datos": ["INTEGER", "VARCHAR", "FLOAT", "VARCHAR", "FLOAT"]
        }}
    ]
}}
```

---

### **Extract the information from the following artifact:**
{codigo}
"""

def extract_metadata(code: str) -> ExtractedEntities:
    response: ParsedChatCompletion[ExtractedEntities] = openai_api_client.beta.chat.completions.parse(
        model="gpt-4o",
        response_format=ExtractedEntities,
        messages=[{"role": "system", "content": EXTRACTION_PROMPT.format(codigo=code)}]
    )

    return response.choices[0].message.parsed

def extract_metadata_with_retries(artifact_code, max_retries=2):
    """
    Intenta extraer metadatos hasta `max_retries` veces si la primera ejecución falla.
    """
    for attempt in range(max_retries):
        print(f"[Neo4j] Extrayendo información del código... (Intento {attempt + 1})")
        extracted_entities = extract_metadata(artifact_code)

        if extracted_entities.apis or extracted_entities.endpoints or extracted_entities.databases \
           or extracted_entities.queries or extracted_entities.tables or extracted_entities.relationships.relaciones:
            return extracted_entities

        print("[Warning] No se encontraron entidades en este intento.")

    print("[Error] No se encontraron entidades después de varios intentos.")
    return extracted_entities