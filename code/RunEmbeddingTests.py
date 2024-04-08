from CosmosDBPyMongoVectorHandler import CosmosDBPyMongoVectorHandler
from LLMHandler import LLMHandler
from AOAIHandler import AOAIHandler
from VectorDBHandler import VectorDBHandler
from Config import Config
def main():
    app_config_data_path = r"C:\Users\dade\Desktop\AzureRAG\config\app_config.json"
    app_config = Config(app_config_data_path)
    DO_INIT = True
    INSERT_DATA = True
    vector_db_handler = None
    vector_db_config = None
    llm_handler = None
    llm_config = None
    (vector_db_handler,vector_db_config) = init_vector_db(app_config)
    (llm_handler,llm_config) = init_LLM(app_config)   
    if(DO_INIT):
        vector_db_handler.reset_db(vector_db_config.config_data)
        vector_db_handler.init_vector_storage(vector_db_config.config_data)
    else:
        vector_db_handler.connect_to_vector_store(vector_db_config.config_data)    
    if(INSERT_DATA):
        data = "This is a test"
        vector = llm_handler.generate_embeddings(data)
        content_to_store = {
            "content": data,
            "contentVector": vector,
            "model": llm_config.config_data["aoai_deployment_name"],
            "company": "Microsoft"
        }
        vector_db_handler.store_vector_data(content_to_store, app_config.config_data)
    test_query = "What is a test?"
    test_vector = llm_handler.generate_embeddings(test_query)
    results = vector_db_handler.do_vector_search(test_vector,app_config.config_data)
    for result in results:
        print(result)
        
def init_vector_db(app_config): 
    vector_db_handler = None
    vector_db_config = None
    if (app_config.config_data["vector_storage_mode"] == "ALL"):
        cosmos_db_config_path = app_config.config_data["cosmos_db_config_path"]
        vector_db_config = Config(cosmos_db_config_path)
        vector_db_handler =  init_cosmos_db(vector_db_config)
    return (vector_db_handler, vector_db_config)

def init_LLM(app_config)->LLMHandler:
    llm_handler = None
    llm_config = None
    if (app_config.config_data["LLM"] == "AOAI"):
        aoai_config_path = app_config.config_data["aoai_config_path"]
        llm_config = Config(aoai_config_path)
        llm_handler = init_AOAI(llm_config)
    return (llm_handler, llm_config)

def init_AOAI(config):
    aoai_endpoint = config.config_data["aoai_endpoint"]
    aoai_key = config.config_data["aoai_key"]
    aoai_api_version = config.config_data["aoai_api_version"]
    aoai_temperature = config.config_data["aoai_temperature"]
    aoai_model = config.config_data["aoai_deployment_name"]
    aoai_handler = AOAIHandler(aoai_endpoint, aoai_key, aoai_api_version, aoai_temperature, aoai_model)
    return aoai_handler
def init_cosmos_db(config):
    cosmos_username = config.config_data["cosmos_username"]
    cosmos_password = config.config_data["cosmos_password"]
    cosmos_server = config.config_data["cosmos_server"]
    cosmos_vector_handler = CosmosDBPyMongoVectorHandler(cosmos_username, cosmos_password, cosmos_server)
    return cosmos_vector_handler
if __name__ == "__main__":
    main()