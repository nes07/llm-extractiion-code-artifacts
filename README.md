# Artifact Knowledge Extraction

## Overview
This project extracts knowledge from code artifacts by identifying APIs, endpoints, queries, databases, tables, and relationships. It structures this extracted knowledge into a Neo4j graph for better visualization and analysis.

## Features
- **API & Endpoint Detection**: Identifies RESTful API calls and their associated endpoints.
- **Query Extraction**: Extracts SQL/NoSQL queries and links them to the relevant databases.
- **Database & Table Identification**: Recognizes databases and their table structures from the provided code.
- **Graph-based Representation**: Stores extracted relationships in Neo4j to enable knowledge graph exploration.
- **Artifact Linking**: Ensures that extracted knowledge is linked to its originating artifact.

## Installation & Setup

This project is designed to run using Docker, Devcontainers, and uv as the package manager.

🐳 Setup using Docker & Devcontainers

The recommended way to set up this project is by using a Devcontainer inside your IDE.

### 1. Ensure you have Docker installed
	•	Install Docker Desktop if you haven’t already.
	•	Make sure Docker is running before proceeding.

### 2. Open the project inside a Devcontainer
	•	If using VSCode, install the Dev Containers extension.
	•	If using IntelliJ, install the Docker Plugin and set up a remote Devcontainer.
	•	Open the project in your IDE and reopen in a Devcontainer when prompted.

### 3. Install dependencies using uv
Once inside the Devcontainer, open a terminal and run:
```sh
uv sync
```

### 4. Set up environment variables:
```sh
cp .env.example .env
```
Edit the `.env` file with your Neo4j credentials.

## Usage
To extract knowledge from an artifact we use the The Artifact Processing system that we created and is now exposed as an API.


### 1. Start the API server
Run the following command to start the API:
```sh
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
You should see an output similar to:
```sh
INFO:     127.0.0.1:60646 - "POST /process_artifact/ HTTP/1.1" 200 OK
```
### 2. Send a JSON Artifact for Processing
You can send an artifact JSON file to the API for processing. Example request:
```sh
curl -X POST "http://127.0.0.1:8000/process_artifact" \
     -H "Content-Type: application/json" \
     -d @artifacts/artifact.json
```

### 3. Verify the API is running
If you want to check if the API is running before making a request:
```sh
curl http://127.0.0.1:8000
```

Expected response:
```sh
{"message":"Artifact Processing API is running!"}
```


## Graph Schema
The system creates the following node types:
- **APINode**: Represents an API service.
- **EndpointNode**: Represents an endpoint within an API.
- **QueryNode**: Represents a database query.
- **DatabaseNode**: Represents a database instance.
- **TableNode**: Represents a table in a database.
- **KPINode**: Represents a key performance indicator (KPI).
- **StatisticNode**: Represents a statistical method used for analysis.
- **ArtifactNode**: Represents the original source artifact.

### Relationships:
- `EXPOSES`: API → Endpoint
- `QUERIES`: Endpoint → Database
- `READS_FROM`: Query → Database
- `STORES`: Database → Table
- `USES`: Table → Query
- `GENERATED`: Artifact → Extracted Nodes

## Author
**Nicolas Espinoza Silva**

For questions or contributions, feel free to reach out.

## License
This project is licensed under the MIT License.
