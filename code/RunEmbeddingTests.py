from CosmosDBPyMongoVectorHandler import CosmosDBPyMongoVectorHandler
from LLMHandler import LLMHandler
from AOAIHandler import AOAIHandler
from VectorDBHandler import VectorDBHandler
from Config import Config
def main():
    config_data_path = r"C:\Users\dade\Desktop\AzureRAG\config\config.json"
    config = Config(config_data_path)
    DO_INIT = True
    INSERT_DATA = True
    vector_db_handler = init_vector_db(config)
    llm_handler = init_LLM(config)
    storage_settings = {
        "batch": False
    }
    search_settings = {
        "num_results": 10
    }
    if(DO_INIT):
        vector_db_handler.reset_db(config.config_data)
        vector_db_handler.init_vector_storage(config.config_data)
    else:
        vector_db_handler.connect_to_vector_store(config.config_data)    
    if(INSERT_DATA):
        data = "This is a test"
        vector = llm_handler.generate_embeddings(data)
        content_to_store = {
            "content": data,
            "contentVector": vector,
            "model": config.config_data["aoai_deployment_name"],
            "company": "Microsoft"
        }
        vector_db_handler.store_vector_data(content_to_store, storage_settings)
    test_query = "What is a test?"
    test_vector = llm_handler.generate_embeddings(test_query)
    results = vector_db_handler.do_vector_search(test_vector,search_settings)
    for result in results:
        print(result)
        
def init_vector_db(config)->VectorDBHandler: 
    if config.config_data["vector_Storage_mode"] == "ALL":
        return init_cosmos_db(config)

def init_LLM(config)->LLMHandler:
    if config.config_data["LLM"] == "AOAI":
        return init_AOAI(config)
    
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