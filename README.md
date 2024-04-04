<h1>Azure RAG Samples repo WIP</h1>

<br/><br/>
Sample config:
{<br/>
    "cosmos_username": "<Username>",<br/>
    "cosmos_password": "<PASSWORD>",<br/>
    "cosmos_server": "<SERVER> (e.g.,myserver.mongocluster.cosmos.azure.com/"),<br/>
    "cosmos_db_name": "<DB_NAME>",<br/>
    "cosmos_db_collection_name": "<COLLECTION_NAME>",<br/>
    "aoai_endpoint": "<AOAI_ENDPOINT>",<br/>
    "aoai_key": "<AOAI_KEY>",<br/>
    "aoai_temperature": <TEMP_SETTING> (e.g., 0.5),<br/>
    "vector_dimension": <VECTOR_SIZE>(e.g., 1536 for AOAI embeddings),<br/>
    "aoai_api_version": "<AOAI_API_VERSION>(e.g., 2024-03-01-preview)",<br/>
    "aoai_deployment_name": "<EMBEDDING_DEPLOYMENT_NAME>",<br/>
    "vector_Storage_mode":"ALL", //Allowed values are "ALL", "COSMOS", or "COGSEARCH"<br/>
    "LLM" : "AOAI"<br/>//Allowed values are "AOAI
}
